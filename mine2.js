const process = await import("process");
const argv = (await import('minimist')).default(process.argv.slice(2));

const yaml = (await import("js-yaml")).default;
const fs = await import("fs");
const fsp = fs.promises;
const path = await import("path");
const url = await import("url");

(async function() {
  const config = yaml.safeLoad(await fsp.readFile("config.yml", 'utf8'));
  global.config = config;
  config.argv = argv;
  config.defines = config.defines || {}; 
  config.defines.CWD = path.dirname(url.fileURLToPath(import.meta.url))+"/";
  const general = await import(config.defines.CWD+"modules/general.js"); general.solveDefines(config.defines);
  global.moduleFolder = process.cwd() + "/modules/";
  global.pipelineFolder = process.cwd() + "/pipelines/";
  
  let pipeline = argv._[0];
  if (pipeline) {
    config.pipeline = config.defines.CWD+`./pipelines/${pipeline}.js`;
    (await import(`./pipelines/${pipeline}.js`)).pipeline_exec(config);
  }
  
}());
