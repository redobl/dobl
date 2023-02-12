var action = tiled.registerAction("SortInventory", function (action) {
    var sel = tiled.activeAsset.selectedObjects;
    if (sel.length != 1) {
        return
    }
    var inv = sel[0].property("Инвентарь");
    if (inv == undefined) {
        return
    }

    var process = new Process();
    var scriptPath = tiled.projectFilePath+tiled.fileSep+"sort.py";
    process.exec("python",[scriptPath,'base64',inv]);
    var result = process.readStdOut();
    sel[0].setProperty("Инвентарь", Qt.atob(result))
})

action.text = "Sort Inventory"

tiled.extendMenu("MapView.Objects", [
    { action: "SortInventory" }
]);