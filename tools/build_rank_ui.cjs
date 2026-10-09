/** Compile the rank-only JSX without shipping Babel in the public site.
 * Usage: node tools/build_rank_ui.cjs path/to/babel-standalone.js
 * Prerequisites: Node.js and a trusted local Babel standalone development copy.
 * The supplied handoff contains Babel 7.29.0, extracted into ignored tmp/.
 */
const fs=require('fs'),vm=require('vm');
if(!process.argv[2]) throw new Error('Pass a trusted local Babel standalone file path');
const context={};
vm.runInNewContext(fs.readFileSync(process.argv[2],'utf8'),context);
if(!context.Babel) throw new Error('Supplied file did not provide Babel');
fs.writeFileSync('assets/site/rank-ui.js',context.Babel.transform(fs.readFileSync('assets/site/rank-ui.jsx','utf8'),{presets:['react'],comments:false,compact:true}).code);
