type RGB = [number, number, number];

export const size = 100;

const hslToRgb = (h: number, s: number, l: number): RGB => {
  s /= size;
  l /= size;

  const k = (n: number) => (n + h / 30) % 12;
  const a = s * Math.min(l, 1 - l);
  const f = (n: number) =>
    l - a * Math.max(-1, Math.min(k(n) - 3, Math.min(9 - k(n), 1)));

  return [
    Math.round(f(0) * 255),
    Math.round(f(8) * 255),
    Math.round(f(4) * 255),
  ];
};

const rgbToHex = (r: number, g: number, b: number): string => {
  const toHex = (n: number) => n.toString(16).padStart(2, "0");
  return `#${toHex(r)}${toHex(g)}${toHex(b)}`;
};

const generateRainbowGradient = (): string[] => {
  const result = new Array<string>(size * size);

  for (let y = 0; y < size; y++) {
    for (let x = 0; x < size; x++) {
      const index = y * size + x;
      const hue = ((x + y) / (2 * size)) * 360; // Interpolating hue

      const [r, g, b] = hslToRgb(hue, size, 50); // Full saturation and medium lightness

      result[index] = rgbToHex(r, g, b);
    }
  }

  return result;
};

const fisherYatesShuffle = <T>(array: T[]): T[] => {
  for (let i = array.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [array[i], array[j]] = [array[j], array[i]];
  }

  return array;
};

export const scramble = () => {
  const og = generateRainbowGradient();
  return { scrambled: fisherYatesShuffle([...og]), unscrambled: og };
};
