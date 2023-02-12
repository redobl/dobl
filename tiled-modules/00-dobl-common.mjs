tiled.fileSep = Qt.platform.os == "windows" ? "\\" : "/"
var sep = tiled.fileSep
var projectFilePathFile = new TextFile("ext:projectFilePath")
var projectFilePath = projectFilePathFile.readLine()
tiled.projectFilePath = projectFilePath