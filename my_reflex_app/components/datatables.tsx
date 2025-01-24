interface Options {
  columns: any;
  buttons: any;
}

export function setRenderFunction(options: Options){
    let columns = options.columns;
    if (columns){
      for (let i = 0; i < columns.length; i++) {
        if (typeof columns[i].render === 'string' && columns[i].render.startsWith("function")){
          columns[i].render = new Function('return ' + columns[i].render)();
        }
      }
    }
  }