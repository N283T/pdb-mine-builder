/*
  Copyright (C) 2021 Gert-Jan Bekker
  gertjan.bekker@gmail.com
*/

const fs = await import("fs");
const fsp = fs.promises;
const readline = await import("readline");
const http = await import("http");
const https = await import("https");
const path = await import("path");
const zlib = await import("zlib");
const child_process = await import("child_process");

const Long = (await import("long")).default;
const picomatch = (await import("picomatch")).default;


export async function walkPattern(pattern, options={}) {
  const base = path.dirname(pattern.substr(0, pattern.indexOf("*")))+"/";
  const matchObj = picomatch(pattern);
  
  const files = [];
  const pattern_handler = function(pth, container) {
    if (! matchObj(pth)) return;
    const obj = {path: pth, name: path.basename(pth)};
    if (options.stats) obj.stats = fsp.stat(pth);
    files.push(obj);
  };
  
  await walk(base, {pattern_handler});
  if (options.stats) {for (const file of files) file.stats = await file.stats;}
  return files;
}

export async function walk(cwd, container) {
  let items;
  try {items = await fsp.readdir(cwd, {withFileTypes: true});}
  catch (e) {console.error(e); return;}
  const jobs = [];
  for (const item of items) {
    const pth = cwd+item.name;
    if (item.isDirectory()) jobs.push(walk(pth+"/", container));
    else container.pattern_handler(pth, container);
  }
  await Promise.all(jobs);
}

export function solveDefines(defines) {
  let N = 0;
  while (true) {
    let bad = false;
    for (const [k,v] of Object.entries(defines)) {
      if (v.indexOf("${") != -1) {
        bad = true;
        defines[k] = expandPath(v);
      }
    }
    if (! bad) break;
    N++;
    if (N > 10) {console.error("Cannot resolve defines..."); process.exit();}
  }
  for (const [k,v] of Object.entries(defines)) defines[k] = path.normalize(expandPath(v));
}

export async function exists(loc) {
  try {await fsp.access(loc, fs.constants.F_OK);}
  catch (e) {return false;}
  return true;
}

export function expandPath(pth) {
  for (let [name, repl] of Object.entries(global.config.defines || {})) pth = pth.replace("${"+name+"}", repl);
  return path.normalize(pth);
}

export function arbitraryPooler(mx) {
  if (new.target === undefined) return new arbitraryPooler(mx);
  this.max = mx;
  this.pool = [];
  this.clients = [];
}

arbitraryPooler.prototype.request = async function() {
  var client; const poolObj = this;
  if (this.clients.length < this.max) {
    client = {}; client.id = this.clients.length; client.release = function() {poolObj.pool.push(this);}; this.clients.push(client);
    return client;
  }
  
  while (true) {
    if (this.pool.length) return this.pool.shift();
    await wait();
  }
};

export function sleep(ms) {return new Promise(resolve=>{setTimeout(resolve,ms)});}
export function wait() {return new Promise(resolve=>{setImmediate(resolve)});}

// cc

export async function mdl2fp(mdl, obabel) {
  var obabelIn = {input: mdl, encoding: 'utf8', stdio: 'pipe'}, smiles, fpt;
  
  try {smiles = (await execCommand(obabel, ["-imdl", "-ocan", "---errorlevel 1"], obabelIn)).trim();}
  catch (e) {}
  if (! smiles) {
    try {smiles = (await execCommand(obabel, ["-imdl", "-osmi", "---errorlevel 1"], obabelIn)).trim();}
    catch (e) {}
  }
  
  if (smiles) {
    obabelIn.input = smiles;
    try {fpt = (await execCommand(obabel, ["-ismi", "-ofpt", "---errorlevel 1"], obabelIn)).trim();}
    catch (e) {}
  }
  else { // mdl input
    obabelIn.input = mdl;
    try {fpt = (await execCommand(obabel, ["-imdl", "-ofpt", "---errorlevel 1"], obabelIn)).trim();}
    catch (e) {}
  }

  fpt = fpt.split("\n"); fpt.splice(0, 1); fpt = fpt.join("").split(" ");
  var fpt_int = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], a, b, i=0;
  while (fpt.length) {
    a = fpt.shift();
    if (fpt.length) b = fpt.shift();
    else b = "";
    fpt_int[i] = Long.fromString(a+b, 16).toString();
    i++;
  }

  return fpt_int;
}

export async function mdl2svg(memObj, obabel) {
  if (! memObj.mdl) cc2mdl(memObj);
  var svg, raw, options = {input: memObj.mdl, encoding: "utf8", stdio: "pipe"};

  try {raw = await execCommand(obabel, ["-xX", "-imdl", "-osvg", "---errorlevel 1", memObj.mdl_noH||""], options);}
  catch (e) {console.log(e);}

  try { // deal with bad svg content from openbabel...
    var tmp = raw.split('viewBox="'); tmp = tmp[tmp.length-1].split('"')[0].split(" ");
    svg = raw.split('stroke-linecap="round">')[1].split("</svg>")[0];
    svg = `<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:cml="http://www.xml-cml.org/schema" width="${tmp[2]}" height="${tmp[3]}" x="0" y="0" font-family="sans-serif" stroke="rgb(0,0,0)" stroke-width="1" stroke-linecap="round" viewBox="0 0 ${tmp[2]} ${tmp[3]}">\n` + svg + "\n</svg>";
  }
  catch (e) {console.error("\n\tSVG failed:", memObj.entryId, options.error, options.stderr, raw, "\n");} // 0CR FDC
  
  return svg || "";
}

export function cc2mdl(memObj) {
  var mmjson = memObj.mmjson;
  
  //console.log(mmjson); //chem_comp_atom
  
  var noha = 0, chem_comp_atom, chem_comp_bond, props = "", mol = "", i, charge, bondType, tmp, obabelIn, svg;

  chem_comp_atom = getObjectValue(mmjson, "chem_comp_atom", {"atom_id": [], "pdbx_model_Cartn_x_ideal": [null]});
  chem_comp_bond = getObjectValue(mmjson, "chem_comp_bond", {"atom_id_1": [], "atom_id_2": []});
  
  var okAtoms = {}, Natoms = 0, Nbonds = 0, idx1, idx2, symbol;
  
  if (chem_comp_atom.pdbx_model_Cartn_x_ideal[0] == null) {
    for (i=0; i<chem_comp_atom.atom_id.length; i++) {
      if (chem_comp_atom.type_symbol[i] != "H" && chem_comp_atom.type_symbol[i] != "D") noha += 1;
      
      charge = chem_comp_atom.charge[i];
      symbol = chem_comp_atom.type_symbol[i].toLowerCase().replace(/^\w/, c => c.toUpperCase());
      mol += `M V30 ${i+1} ${symbol} ${(chem_comp_atom.model_Cartn_x[i] || 0.0).toFixed(3)} ${(chem_comp_atom.model_Cartn_y[i] || 0.0).toFixed(3)} ${(chem_comp_atom.model_Cartn_z[i] || 0.0).toFixed(3)} 0` + (charge ? " CHG="+charge : "") + "\n";
      
      okAtoms[chem_comp_atom.atom_id[i]] = Natoms;
      Natoms++;
    }
  }
  else {
    for (i=0; i<chem_comp_atom.atom_id.length; i++) {
      if (chem_comp_atom.type_symbol[i] != "H" && chem_comp_atom.type_symbol[i] != "D") noha += 1;
      
      charge = chem_comp_atom.charge[i];
      symbol = chem_comp_atom.type_symbol[i].toLowerCase().replace(/^\w/, c => c.toUpperCase());
      mol += `M V30 ${i+1} ${symbol} ${(chem_comp_atom.pdbx_model_Cartn_x_ideal[i] || 0.0).toFixed(3)} ${(chem_comp_atom.pdbx_model_Cartn_y_ideal[i] || 0.0).toFixed(3)} ${(chem_comp_atom.pdbx_model_Cartn_z_ideal[i] || 0.0).toFixed(3)} 0` + (charge ? " CHG="+charge : "") + "\n";
      
      okAtoms[chem_comp_atom.atom_id[i]] = Natoms;
      Natoms++;
    }
  }

  mol += "M V30 END ATOM\nM V30 BEGIN BOND\n";
  
  for (i=0; i<chem_comp_bond.atom_id_1.length; i++) {
    idx1 = okAtoms[chem_comp_bond.atom_id_1[i]];
    idx2 = okAtoms[chem_comp_bond.atom_id_2[i]];
    if (idx1 === undefined || idx2 === undefined) continue;
    bondType = chem_comp_bond.value_order[i].toLowerCase();
    if (bondType == "sing") bondType = "1";
    else if (bondType == "doub") bondType = "2";
    else if (bondType == "trip") bondType = "3";
    
    mol += `M V30 ${i+1} ${bondType} ${idx1+1} ${idx2+1}\n`;
    
    Nbonds++;
  }
  
  mol = `\n\n\n 0 0 0 0 0 999 V3000
M V30 BEGIN CTAB
M V30 COUNTS ${Natoms} ${Nbonds} 0 0 1
M V30 BEGIN ATOM
${mol}M V30 END BOND
M V30 END CTAB
M END`;

  memObj.mdl = mol;
  memObj.mdl_noH = noha > 1 ? "-d" : "";
  memObj.mdl_Natoms = Natoms;
};

// end cc

export function getObjectValue(object, field, defaultValue) {
  if (field in object) return object[field];
  else return defaultValue;
}

export function execCommand(cmd, args, options) {
  options = options || {};
  const promise = new Deferred();
  const proc = child_process.execFile(cmd, args, function(error, stdout, stderr) {
    if (options.extended) promise.resolve([error, stdout, stderr]);
    else {
      options.error = error;
      options.stderr = stderr;
      promise.resolve(stdout);
    }
  });
  if (options.input) {
    proc.stdin.write(options.input);
    proc.stdin.end();
  }
  return promise.promise;
}

export async function *walkdir(loc) {
  var items = await fsp.readdir(loc, {withFileTypes: true});
  for (let i of items) {
    if (i.isDirectory()) yield *walkdir(loc+"/"+i.name);
    else yield loc+"/"+i.name;
  }
}

export function Deferred() {
  var self = this;
  this.promise = new Promise(function(resolve, reject) {
    self.reject = reject
    self.resolve = resolve
  })
}

export function gzip(input, options) {
  const promise = new Promise(function(resolve, reject) {
    zlib.gzip(input, options, function (error, result) {
      if(!error) resolve(result);
      else reject(Error(error));
    });
  });
  return promise;
}

export function gunzip(input, options) {
  const promise = new Promise(function(resolve, reject) {
    zlib.gunzip(input, options, function (error, result) {
      if(!error) resolve(result);
      else reject(Error(error));
    });
  });
  return promise;
}

export async function readlineGZ(loc, todo) {
  var promise = new Deferred();
  
  var inp = fs.createReadStream(loc);
  if (loc.endsWith(".gz")) inp = inp.pipe(zlib.createGunzip());
  inp.on("error", function() {
    promise.reject();
  });
  
  const readInterface = readline.createInterface({
    input: inp,
    console: false
  });
  readInterface.on('line', todo);
  
  readInterface.on('close', function() {
    promise.resolve();
  });
  
  
  return promise.promise;
}

