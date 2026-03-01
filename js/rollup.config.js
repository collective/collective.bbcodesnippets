import resolve from "@rollup/plugin-node-resolve";
import terser from "@rollup/plugin-terser";
import commonjs from "@rollup/plugin-commonjs";

const outputDir = "../src/collective/bbcodesnippets/static";

export default {
  input: "src/main.js",
  output: [
    {
      file: `${outputDir}/collective.bbcodesnippets.js`,
      format: "iife",
      name: "collectivebbcodesnippets",
      sourcemap: true,
    },
    {
      file: `${outputDir}/collective.bbcodesnippets.min.js`,
      format: "iife",
      name: "collectivebbcodesnippets",
      plugins: [terser()],
    },
  ],
  plugins: [resolve({ browser: true }), commonjs()],
};
