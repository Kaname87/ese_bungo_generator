import { IncomingMessage, ServerResponse } from "http";
import { parseRequest } from "./_lib/parser";
import { getHtml } from "./_lib/template";
// import { writeTempFile } from "./_lib/file";
import { getScreenshot } from "./_lib/chromium";

const isDev = process.env.NOW_REGION === "dev1";

export default async function handler(
  req: IncomingMessage,
  res: ServerResponse
) {
  try {
    const parsedReq = parseRequest(req);
    console.log(parsedReq)
    const html = getHtml(parsedReq);

    // return renderHtml(res, html)

    const file = await getScreenshot(html, "png", isDev);

    res.statusCode = 200;
    res.setHeader("Content-Type", "image/jpeg");
    res.setHeader(
      "Cache-Control",
      "public,immutable,no-transform,s-max-age=21600,max-age=21600"
    );
    res.end(file);
  } catch (e) {
    res.statusCode = 500;
    res.setHeader("Content-Type", "text/html");
    res.end("<h1>Internal Error</h1><p>nazeda..</p>");
    console.error(e);
  }
}

const renderHtml = (res: ServerResponse, html: string) => {
  res.statusCode = 200;
  res.setHeader("Content-Type", "text/html");
  res.end(html);
};
