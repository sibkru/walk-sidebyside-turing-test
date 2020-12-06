function GetURLParameter(sParam)
{
    var sPageURL = window.location.search.substring(1);
    var sURLVariables = sPageURL.split('&');
    for (var i = 0; i < sURLVariables.length; i++) 
    {
        var sParameterName = sURLVariables[i].split('=');
        if (sParameterName[0] == sParam) 
        {
            return sParameterName[1];
        }
    }
}

function initShaderProgram(gl, vsSource, fsSource) {
    const vertexShader = loadShader(gl, gl.VERTEX_SHADER, vsSource);
    const fragmentShader = loadShader(gl, gl.FRAGMENT_SHADER, fsSource);

    // Create the shader program

    const shaderProgram = gl.createProgram();
    gl.attachShader(shaderProgram, vertexShader);
    gl.attachShader(shaderProgram, fragmentShader);
    gl.linkProgram(shaderProgram);

    // If creating the shader program failed, alert

    if (!gl.getProgramParameter(shaderProgram, gl.LINK_STATUS)) {
    alert('Unable to initialize the shader program: ' + gl.getProgramInfoLog(shaderProgram));
    return null;
    }

    return shaderProgram;
}

function loadShader(gl, type, source) {
    const shader = gl.createShader(type);

    // Send the source to the shader object
    gl.shaderSource(shader, source);

    // Compile the shader program
    gl.compileShader(shader);

    // See if it compiled successfully
    if (!gl.getShaderParameter(shader, gl.COMPILE_STATUS)) {
        alert('An error occurred compiling the shaders: ' + gl.getShaderInfoLog(shader));
        gl.deleteShader(shader);
        return null;
    }

    return shader;
}

function loadFile(filePath) {
    var result = null;
    var xmlhttp = new XMLHttpRequest();
    xmlhttp.open("GET", filePath, false);
    xmlhttp.send();
    if (xmlhttp.status==200) {
        result = xmlhttp.responseText;
    }
    return result;
}

function createTrajectory(trial) {
    var train = loadFile(trial.fn_train).split('\n').slice(1);
    path1 = train
    console.log(trial)
    if (!trial.catch_trial) {
        console.log(trial.fn.split('/')[2])
    } else {
        console.log("Catchtrial", trial.offset, trial.order)
    }
    if (trial.natural){
        var path2 = train;
    } 
    else {
        if (trial.catch_trial) {
            var path2 = path1.slice(trial.offset);
            // var path2 = path1.slice();
            // for (var i = 0; i < trial.offset; ++i) {
            //     path2.unshift("");
            // }
        } else {
            var model = loadFile(trial.fn).split('\n');
            var path2 = model;
        }
    }

    const dofs = path1[0].split(";").length
    var lines = [];
    for (var j = 0; j < path2.length-1; ++j){
        if (j < trial.occ_start) {
            lines.push(path1[j].split(";").map(parseFloat));
        } else if (j > trial.occ_end) {
            lines.push(path2[j].split(";").map(parseFloat));
        } else {
            lines.push(new Array(dofs).fill(-1000.0));
        }
    }
    return lines
}

function setupCanvas() {
    const canvas = document.createElement('canvas');
    canvas.setAttribute('id', 'glcanvas');
    canvas.width = 440;
    canvas.height = 480;
    canvas.setAttribute("z-index", 9999);
    document.getElementById('jspsych-content').appendChild(canvas);
}

function resize(canvas) {
    // Lookup the size the browser is displaying the canvas.
    var displayWidth  = canvas.clientWidth;
    var displayHeight = canvas.clientHeight;

    // Check if the canvas is not the same size.
    if (canvas.width  != displayWidth ||
      canvas.height != displayHeight) {

    // Make the canvas the same size
    canvas.width  = displayWidth;
    canvas.height = displayHeight;
    }
}

function minimizeCanvas() {
    const canvas = document.getElementById('glcanvas')
    canvas.width = 40;
    canvas.height = 80;
}

