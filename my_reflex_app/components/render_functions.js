function showHamburger(data, type, row, meta) {
    console.log(data, type, row, meta);
    return '≡'; 
}

function render_input_cell(data, type, row, meta) {
    if (type === 'export') {
        return data
    }
    return `<input type="number" class="ai-input dt-input"   type="number" value="${data}" min="0" step="1"/>`;
}