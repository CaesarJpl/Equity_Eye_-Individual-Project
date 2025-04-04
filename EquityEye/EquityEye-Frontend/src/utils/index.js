export const loadFiles = (filename)=> {
    return new Promise((resolve, reject) => {
        const filesContext = require.context('../../data/stocks_JSON', false, /\.json$/);
        const matchedFiles = filesContext.keys().filter(filePath => {
            const name = filePath.replace(/(\.\/|\.json)/g, '');
            return name === filename;
        });
        if (matchedFiles.length > 0) {
            const json = filesContext(matchedFiles[0]);
            resolve(json);
        } else {
            reject(new Error(`File with name "${filename}" not found.`));
        }
    });

}