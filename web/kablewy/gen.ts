import { writeFileSync, appendFileSync } from "fs";
import { join } from "path";

const flag = "LITCTF{k3F7zH}";
const mainTsPath = join(__dirname, "src/main.ts");
writeFileSync(mainTsPath, "");

// Start with a clean main.ts file
writeFileSync(mainTsPath, "const workers = [];\n");

flag.split("").forEach((char, index) => {
  const script = `while (true) console.log('kablewy');\npostMessage('${char}');`;
  const encodedScript = btoa(script);

  const decodeEvalScript = `eval(atob('${encodedScript}'))`;

  // Write each worker script
  writeFileSync(join(__dirname, `src/workers/${index}.ts`), decodeEvalScript);

  // Append import statement for the worker in main.ts
  const workerImportPath = `./workers/${index}.ts?worker&inline`;
  appendFileSync(
    mainTsPath,
    `import Worker${index} from '${workerImportPath}';\nworkers.push(Worker${index});\n`
  );
});

appendFileSync(mainTsPath, "workers.forEach(worker => new worker());\n");
