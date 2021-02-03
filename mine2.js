//const fs = await import("fs");
//const fsp = fs.promises;
//const readline = await import("readline");
//const zlib = await import("zlib");

//const cif = await import("./modules/cif.js");
//const general = await import("./modules/general.js");

const process = await import("process");
const argv = (await import('minimist')).default(process.argv.slice(2));

// node mine2.js --pipeline=internal.import_mmcif 

// -pipeline

const yaml = (await import("js-yaml")).default;
const fs = await import("fs");
const fsp = fs.promises;
const path = await import("path");
const url = await import("url");

(async function() {
  const config = yaml.safeLoad(await fsp.readFile("config.yml", 'utf8'));
  config.argv = argv;
  config.defines = config.defines || {}; 
  config.defines.CWD = path.dirname(url.fileURLToPath(import.meta.url))+"/";
  
  global.moduleFolder = process.cwd() + "/modules/";
  global.pipelineFolder = process.cwd() + "/pipelines/";
  
  let pipeline = argv._[0];
  if (pipeline) {
    config.pipeline = config.defines.CWD+`./pipelines/${pipeline}.js`;
    (await import(`./pipelines/${pipeline}.js`)).pipeline_exec(config);
  }
  
}());
