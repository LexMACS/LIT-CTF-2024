const workers = [];
import Worker0 from "./workers/0.ts?worker&inline";
workers.push(Worker0);
import Worker1 from "./workers/1.ts?worker&inline";
workers.push(Worker1);
import Worker2 from "./workers/2.ts?worker&inline";
workers.push(Worker2);
import Worker3 from "./workers/3.ts?worker&inline";
workers.push(Worker3);
import Worker4 from "./workers/4.ts?worker&inline";
workers.push(Worker4);
import Worker5 from "./workers/5.ts?worker&inline";
workers.push(Worker5);
import Worker6 from "./workers/6.ts?worker&inline";
workers.push(Worker6);
import Worker7 from "./workers/7.ts?worker&inline";
workers.push(Worker7);
import Worker8 from "./workers/8.ts?worker&inline";
workers.push(Worker8);
import Worker9 from "./workers/9.ts?worker&inline";
workers.push(Worker9);
import Worker10 from "./workers/10.ts?worker&inline";
workers.push(Worker10);
import Worker11 from "./workers/11.ts?worker&inline";
workers.push(Worker11);
import Worker12 from "./workers/12.ts?worker&inline";
workers.push(Worker12);
import Worker13 from "./workers/13.ts?worker&inline";
workers.push(Worker13);
for (let i = 0; i < 100; i++) new bg();
let str = "";
(async () => {
  for (const worker of workers) {
    const w = new worker();
    str += await new Promise<string>((resolve) => {
      w.onmessage = (e) => {
        resolve(e.data);
      };
    });
    w.terminate();
  }
})();

import bg from "./bgWorker?worker&inline";
