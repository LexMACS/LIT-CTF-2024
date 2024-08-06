import http from "http";
import fs from "node:fs/promises";
import path from "node:path";
import url from "node:url";

const server = http.createServer(async (req, res) => {
  // Parse the raw URL to get the path
  const rawPath = decodeURIComponent(req.url!);

  // Resolve the absolute path, allowing for parent directory access
  const absPath = path.join(__dirname, "site", rawPath);

  try {
    const file = await fs.readFile(absPath, "utf-8");
    res.writeHead(200, { "Content-Type": "text/plain" });
    res.end(file);
  } catch {
    try {
      const indexFile = await fs.readFile(path.join(absPath, "index.html"), "utf-8");
      res.writeHead(200, { "Content-Type": "text/html" });
      res.end(indexFile);
    } catch {
      res.writeHead(404, { "Content-Type": "text/plain" });
      res.end("404 not found");
    }
  }
});

server.listen(process.env.PORT || 3000, () => {
  console.log("Server started");
});
