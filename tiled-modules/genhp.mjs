var action = tiled.registerAction("GenHP", function (action) {
    var spentSP = tiled.prompt("How much SP spent on HP?");
    var process = new Process();
    var scriptPath = tiled.projectFilePath+"\\generate.py"

    process.exec("python",[scriptPath,"hp","100",spentSP]);
    var result = process.readLine();
    result = result.replace(/\r?\n?[^\r\n]*$/, "")

    var sel = tiled.activeAsset.selectedObjects;
    if (sel.length == 1) {
        sel[0].setProperty("Очки Здоровья", result+"/"+result+" ("+result+")")
    }
})

action.text = "Generate HP"

tiled.extendMenu("MapView.Objects", [
    { action: "GenHP" }
]);