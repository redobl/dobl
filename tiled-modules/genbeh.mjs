var action = tiled.registerAction("GenBehavior", function (action) {
    var process = new Process();
    var scriptPath = tiled.projectFilePath+tiled.fileSep+"generate.py"

    process.exec("python",[scriptPath,"behavior"]);
    var result = process.readLine();
    if (result.includes("\n")) {
        // remove everything after newline
        result = result.replace(/\r?\n?[^\r\n]*$/, "")
    }

    var sel = tiled.activeAsset.selectedObjects;
    if (sel.length == 1) {
        sel[0].setProperty("Поведение", result)
    }
})

action.text = "Generate Behavior"

tiled.extendMenu("MapView.Objects", [
    { action: "GenBehavior" }
]);