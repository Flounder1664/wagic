import zipfile, os

core = r"M:\Claude_projects\wagic\projects\mtg\bin\Res\core.zip"
modrules_src = r"M:\Claude_projects\wagic\projects\mtg\bin\Res\rules\modrules.xml"
core_tmp = core + ".tmp"

with open(modrules_src, "rb") as f:
    new_xml = f.read()

with zipfile.ZipFile(core, "r") as zin, zipfile.ZipFile(core_tmp, "w", zipfile.ZIP_DEFLATED) as zout:
    for item in zin.infolist():
        if item.filename == "rules/modrules.xml":
            print("Replacing: " + item.filename)
            zout.writestr(item, new_xml)
        else:
            zout.writestr(item, zin.read(item.filename))

os.replace(core_tmp, core)
print("Done. core.zip updated with new modrules.xml")
print("Size: " + str(os.path.getsize(core)) + " bytes")
