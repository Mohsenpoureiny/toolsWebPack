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
  for (var index = 0; index < totalfiles; index++) {
    data.append("files[]", document.getElementById('files').files[index]);
  }
  data.append("category", $("#category").val())
  axios.post('/add/file', data, config)
    .then(res => window.location.href = "/")
    .catch(err => alert("مشکلی پیش آمده!"))
}

