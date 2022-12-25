const fs = require("fs");
const si = require("search-index");

function isValidUrl(str) {
  var pattern = new RegExp(
    "^(https?:\\/\\/)?" + // protocol
      "((([a-z\\d]([a-z\\d-]*[a-z\\d])*)\\.)+[a-z]{2,}|" + // domain name
      "((\\d{1,3}\\.){3}\\d{1,3}))" + // OR ip (v4) address
      "(\\:\\d+)?(\\/[-a-z\\d%_.~+]*)*" + // port and path
      "(\\?[;&a-z\\d%_.~+=-]*)?" + // query string
      "(\\#[-a-z\\d_]*)?$",
    "i"
  ); // fragment locator
  return !!pattern.test(str);
}

fs.readFile("./data.json", function (err, res) {
  // Check for errors
  if (err) throw err;

  // Converting to JSON
  const data = JSON.parse(res).links;

  //   console.log(data); // Print users

  data.forEach((link) => {
    // if (isValidUrl(link))
    fs.appendFileSync("links.txt", link + "\n");
  });
  //   var links = fs.readFileSync("links.txt", "utf8");

  //   fs.appendFileSync("links.txt", "w");
});
