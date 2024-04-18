const express = require('express');
const path = require('path');
const app = express();

app.use(express.static(path.join(__dirname, 'public'))); // Serve static files from the public directory

app.get('/bom', (req, res) => {
    res.redirect('https://lsattachiris.notion.site/IMECHE-STREETCH-BOM-975d8fde7d7a442c84cb670cf4722836?pvs=4');
});

app.get('/poster', (req, res) => {
    res.redirect('https://www.canva.com/design/DAGCftDCVQQ/hcSXp3mZOZXagdH0uZIf2g/view?utm_content=DAGCftDCVQQ&utm_campaign=designshare&utm_medium=link&utm_source=editor');
});

app.get(['/video', '/presentation'], (req, res) => {
    res.redirect('https://www.loom.so');
});

app.get('/cad', (req, res) => {
    res.sendFile(__dirname + '/cad.html');
});

app.get(['/dijkstra', '/path'], (req, res) => {
    res.sendFile(__dirname + '/dijkstra.html');
});

app.get(['/code', '/arduino'], (req, res) => {
    res.sendFile(__dirname + '/code.html');
});

app.get('/', (req, res) => {
    res.sendFile(__dirname + '/index.html');
});

app.get('*', (req, res) => {
    res.sendFile(__dirname + '/index.html');
});

const PORT = process.env.PORT || 3000;

app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});

