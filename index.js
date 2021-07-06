const express = require('express');
const fs = require('fs-extra');
const bodyParser= require('body-parser');
const { Client } = require('pg');

const app = express();
app.use(express.static('static'));
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: false }));

const client = new Client({
  connectionString: process.env.DATABASE_URL,
  ssl: {
    rejectUnauthorized: false
  }
});

client.connect();


app.post('/saveConsent', (req, res) => {
  fs.appendFile('consent.txt', JSON.stringify(req.body), function (err) {
    if (err) return console.log(err);
  });
}
);

app.post('/saveData', (req, res) => {
  const fileName = "./data/" + req.body.filename + ".json";
  const fileData = req.body.filedata;
  fs.ensureFileSync(fileName)
  fs.writeFile(fileName, JSON.stringify(fileData), function (err) {
    if (err) return console.log(err);
  });
}
);

const PORT = process.env.PORT || 3000;
app.listen(PORT, err => {
    if(err) throw err;
    console.log("%c Server running", "color: green");
});