let s = `࠴࠱࠼ࠫ࠼࠮ࡣࡋࡍࠨ࡛ࡍ࡚ࡇ࡛ࠩࡔࡉࡌࡥ`;
let ord = c => c.codePointAt(0);
let chr = i => String.fromCodePoint(i);
console.log([...s].map(c=>chr(ord(c)-ord(s.at(0))+ord("L"))).join(""));
