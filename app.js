/* ----- Loading Packages  ----- */
const compression = require("compression");
const express = require("express");
const cookieParser = require("cookie-parser");
const logger = require("morgan");
const helmet = require("helmet");

/* ----- Initial Configuration  ----- */
const app = express();

/* ----- Packages  ----- */
app.use(logger("dev"));
app.disable('x-powered-by')
app.use(express.urlencoded({ extended: true }));
app.use(cookieParser());
app.use(compression());
app.use(helmet({
    contentSecurityPolicy: false,
}));
app.disable('x-powered-by')

/* ----- Loading Routes  ----- */
app.set("view engine", "ejs");
app.engine('ejs', require('ejs').__express);
app.set("views", [__dirname + "/pages"]);
app.use(express.static(__dirname + "/public"));

/* ----- Routing ----- */
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
    res.render(__dirname + '/cad.html');
});

app.get(['/dijkstra', '/path'], (req, res) => {
    res.render(__dirname + '/dijkstra.html');
});

app.get(['/code', '/arduino'], (req, res) => {
    res.render(__dirname + '/code.html');
});

app.get('/', function (req, res) {
    res.render("index");
})

app.get('/ar', function (req, res) {
    res.render("ar");
})

app.get('*', (req, res) => {
    res.render(__dirname + '/index.ejs');
});

/* ----- Server ----- */
app.use(function (err, req, res, next) {
    res.locals.message = err.message;
    res.locals.error = req.app.get("env") === "production" ? err : {};

    if (req.app.get("env") === "development") {
        // Show detailed error information for developers
        res.status(err.status || 500);
        res.json({
            error: {
                code: err.status || 500,
                name: err.name,
                message: err.message,
                stack: err.stack,
            }
        });
    } else {
        res.status(err.status || 500);
        res.render("error");
    }
});

app.get("*", function (req, res, next) {
    var err = new Error();
    err.status = 404;
    next(err);
});

app.use(function (req, res, next) {
    if (req.secure) {
        res.setHeader('Strict-Transport-Security', 'max-age=31536000; includeSubDomains; preload');
    }
    next();
})

app.use(function (err, req, res, next) {
    if (err.status === 404) {
        res.status(404).render("error");
    } else {
        return next();
    }
});

const port = process.env.PORT || 3000;
app.listen(port, () => {
    console.log("Server is listening on: ", port);
});