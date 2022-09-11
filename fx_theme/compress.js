/**
 * ugly and compress the js
 */
let UglifyJS = require("uglify-js");
let fs = require("fs");
let path = require("path")

function _compress(dir) {
    const files = fs.readdirSync(dir)
    files.forEach(function (tmpFile, index) {
        if (tmpFile == 'compress.js' || !tmpFile) {
            return
        }
        let file_path = path.join(dir, tmpFile)
        let stat = fs.lstatSync(file_path)
        if (stat.isFile()) {
            let code = fs.readFileSync(file_path, "utf8");
            let uglifyCode = UglifyJS.minify(code, {
                mangle: { reserved: ['require', '_super'] }
            }).code;
            let fd = fs.openSync(file_path, 'w');
            fs.writeFileSync(fd, uglifyCode);
            fs.closeSync(fd);
        } if (stat.isDirectory() && tmpFile != '.' && tmpFile != '..') {
            _compress(file_path)
        }
    })
}

_compress('./static/js/')


