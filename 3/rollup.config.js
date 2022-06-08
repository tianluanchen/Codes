import { defineConfig } from 'rollup';
import commonjs from "@rollup/plugin-commonjs"
import { terser } from 'rollup-plugin-terser';
export default defineConfig([
    {
        input: './index.js',
        output: {
            file: "./dist/gh-readme-md-gen.min.js",
            format: 'umd',
            name: 'grs',
            compact: true
        },
        plugins: [commonjs(), terser()]
    },
    {
        input: './quickstart.js',
        output: {
            file: "./dist/quickstart.min.js",
            format: 'iife',
            compact: true
        },
        plugins: [commonjs(), terser()]
    }

]);