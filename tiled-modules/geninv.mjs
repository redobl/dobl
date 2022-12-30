var action = tiled.registerAction("GenInventory", function (action) {
    var spentSP = tiled.prompt("How many items?");
    var process = new Process();
    var scriptPath = tiled.projectFilePath+"\\generate.py"
    
    process.exec("python",[scriptPath,"item_base64",spentSP]);
    var result = process.readLine();
    
    var sel = tiled.activeAsset.selectedObjects;
    if (sel.length == 1) {
        sel[0].setProperty("Инвентарь", Qt.atob(result))
    }
})

action.text = "Generate Inventory"

tiled.extendMenu("MapView.Objects", [
    { action: "GenInventory" },
    { separator: true }
]);