var express = require('express');
var app = express();

app.use((req, res, next) => {
  console.log(decodeURIComponent(req.originalUrl));
  next();
})

app.use(express.static(__dirname + "/public"));

app.listen(3000, 'localhost', () => {
  console.log("listening!")
});
