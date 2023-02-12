var action = tiled.registerAction("GenAbilities", function (action) {
    var spentSP = tiled.prompt("How many abilities?");
    var scriptPath = tiled.projectFilePath+tiled.fileSep+"generate.py"
    
    var skills = [];
    var traits = [];
    var skillCount = 0;
    var traitCount = 0;
    var failed = 0;

    for (var i = 0; i < spentSP; i++) {
        var process = new Process();
        process.exec("python",[scriptPath,"ability_base64",spentSP]);
        var abil = Qt.atob(process.readLine());
        var abilType = abil[0];
        var abilName = abil.slice(1);
        if (abilType == "s") {
            if (skillCount < 10-traitCount) {
                skills.push((skillCount+1).toString()+". "+abilName);
                skillCount++;
            } else {
                failed++;
            }
        } else if (abilType == "t") {
            if (traitCount < Math.min(5, 10-skillCount)) {
                traits.push((traitCount+1).toString()+". "+abilName);
                traitCount++;
            } else {
                failed++;
            }
        }
    }
    var skillsResult = skills.join("\n");
    var traitsResult = traits.join("\n");

    var sel = tiled.activeAsset.selectedObjects;
    if (sel.length == 1) {
        sel[0].setProperty("Навыки", skillsResult)
        sel[0].setProperty("Особенности", traitsResult)
    }
    if (failed > 0) {
        tiled.alert("Failed to generate "+failed.toString()+" abilities, returning them as SP", "Not enough ability slots");
        var sp = sel[0].property("Очки Души");
        if (sp == undefined) {
            sp = 0;
        }
        // TODO: replace with setFloatProperty as soon as 1.9.3 releases
        sel[0].setProperty("Очки Души", sp+failed);
    }
})

action.text = "Generate Abilities"

tiled.extendMenu("MapView.Objects", [
    { action: "GenAbilities" }
]);