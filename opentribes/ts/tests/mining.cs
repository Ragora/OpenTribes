// -----------------------------------------------------
// Datablocks
// Note: You can't actually target interiors with beams,
// so make an interior and put this box around it.
// -----------------------------------------------------
datablock StaticShapeData(MiningBox) : StaticShapeDamageProfile {
	className = "MineBox";
	shapeFile = "Pmiscf.dts";

	maxDamage      = 5000;
	destroyedLevel = 0;
	disabledLevel  = 0;

	isShielded = false;
	energyPerDamagePoint = 240;

	dynamicType = $TypeMasks::StaticShapeObjectType;
	deployedObject = true;
	cmdCategory = "DSupport";
	cmdIcon = CMDSensorIcon;
	cmdMiniIconName = "commander/MiniIcons/com_deploymotionsensor";
	targetNameTag = 'Mining Detection Box';
	deployAmbientThread = true;
	debrisShapeName = "debris_generic_small.dts";
	debris = DeployableDebris;
	heatSignature = 0;
	needsPower = false;
};

// -----------------------------------------------------
// Code
// Note: Weapon code is in weapons/miningTool.cs
// -----------------------------------------------------
function MiningBox::onAdd(%this, %obj)
{
	%obj.startFade(1,0,1);
	%obj.applyDamage(%obj.getDataBlock().maxDamage); //Start the rock off
}
