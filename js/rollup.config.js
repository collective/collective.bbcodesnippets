import resolve from '@rollup/plugin-node-resolve';
import {terser} from 'rollup-plugin-terser';
import commonjs from '@rollup/plugin-commonjs';

export default {
	input: 'src/main.js',
	output: [{
		sourcemap: true,
		format: 'iife',
		name: 'collectivebbcodesnippets',
		file: '../src/collective/bbcodesnippets/static/collective.bbcodesnippets.js'
	},
    {
		file: '../src/collective/bbcodesnippets/static/collective.bbcodesnippets.min.js',
		format: 'iife',
		name: 'version',
		plugins: [terser()]
	  }
	],
	plugins: [
		resolve({
			browser: true,
		}),	
		commonjs(),
	]
}
