import chromium from "chrome-aws-lambda";
import fs from "fs";
const exePath = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome";

interface Options {
  args: string[];
  executablePath: string;
  headless: boolean;
}

export async function getOptions(isDev: boolean) {


  let isExist = await fs.existsSync(`${process.cwd()}/pages/api/_fonts/nishiki.otf`);
  console.log(isExist)
  await chromium.font(`${process.cwd()}/pages/api/_fonts/nishiki.otf`);

  console.log(chromium.font)
  let options: Options;
  if (isDev) {
    options = {
      args: [],
      executablePath: exePath,
      headless: true,
    };
  } else {
    options = {
      args: chromium.args,
      executablePath: await chromium.executablePath,
      headless: chromium.headless,
    };
  }
  return options;
}
