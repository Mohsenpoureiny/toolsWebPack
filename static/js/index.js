let content = null;
if ("serviceWorker" in navigator) {
  navigator.serviceWorker
    .register("./static/serviceWorker.js")
    .then(reg => {
      console.log("Service worker registred successfully", reg);
    })
    .catch(err => {
      console.log("service worker not registred !!", err);
    });
}
function upload() {
  const config = {
    onUploadProgress: function (progressEvent) {
      var percentCompleted = Math.round((progressEvent.loaded * 100) / progressEvent.total);
      $("#progress").width(`${percentCompleted}%`);
      $("#progress-percent").text(`${percentCompleted}%`);
    }
  }

  let data = new FormData()
  var totalfiles = document.getElementById('files').files.length;
  var folder = document.getElementById('folder').files.length;
  // if (content !== null)
  //   for (var index = 0; index < content.length; index++) {
  //     data.append("files[]", content[index]);
  //   }
  // else
  for (var index = 0; index < totalfiles; index++) {
    data.append("files[]", document.getElementById('files').files[index]);
  }
  for (var index = 0; index < folder; index++) {
    data.append("files[]", document.getElementById('folder').files[index]);
  }
  data.append("category", $("#category").val())
  axios.post('/add/file', data, config)
    .then(res => { window.location.href = "/" })
    .catch(err => alert("مشکلی پیش آمده!"))
}

// function uploadfolder(event) {
//   console.log(event);
//   var fileslist = event.target.files;
//   content = fileslist;
// }
// var fileElem = document.getElementById("files");
// var fileSelected = null;
// if (fileElem) fileElem.onclick = function (e) {
//   fileSelected = this.value;
//   this.value = null;
// };
/* or use this in your browse() function:
    fileElem.value = null;
*/
// if (fileElem) fileElem.onchange = function (e) { // will trigger each time
//   uploadfolder(e);
//   // handleFileDialog(this.value === fileSelected);
// };
