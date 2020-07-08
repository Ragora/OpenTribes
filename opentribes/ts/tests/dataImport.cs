//------------------------------------------------------------------------------
// scripts/modScripts/server/dataImport.cs
//------------------------------------------------------------------------------

function gameConnection::writeSaveFile(%this)
{
	//Compile Main Variable List
	%mission = $CurrentMission;
	%player = %this.player;
	%transform = %player.getTransform();
	%velocity = %player.getVelocity();
	%damage = %player.getDamageLevel();
	%race = %this.race;
	%armor = %this.armor;
	%energy = %player.getEnergyLevel();
	%whiteout = %player.getWhiteout();
	%damageFlash = %player.getDamageFlash();
	%cash = %this.cash;
	%hasRadio = %this.hasRadio;
	%underStandsHuman = %this.underStandsHuman;
	%underStandsBioderm = %this.underStandsBioderm;
	%underStandsDraakan = %this.underStandsDraakan;
	%underStandsCriollos = %this.underStandsCriollos;

	%time = formatTimeString("hh:nn A");
	%date = formatTimeString("mm/dd/yy");

	%file = "data/game/saves/" @ %mission @ "/" @ %this.guid @ ".txt";
	%fileObj = new fileObject();
	%fileObj.openForWrite(%file);
	%fileObj.writeLine(";Saved by" SPC %this.nameBase SPC "on" SPC %date SPC "at" SPC %time);
	%fileObj.writeLine("");

	//Todo: Make this writing method more efficient ...
	%fileObj.writeLine("[Character]");
	%fileObj.writeLine("transform = \x22" @ %transform @ "\x22;");
	%fileObj.writeLine("velocity = \x22" @ %velocity @ "\x22;");
	%fileObj.writeLine("damage = \x22" @ %damage @ "\x22;");
	%fileObj.writeLine("race = \x22" @ %race @ "\x22;");
	%fileObj.writeLine("armor = \x22" @ %armor @ "\x22;");
	%fileObj.writeLine("energy = \x22"  @ %energy @ "\x22;");
	%fileObj.writeLine("whiteOut = \x22" @ %whiteout @ "\x22;");
	%fileObj.writeLine("damageFlash = \x22" @ %damageFlash @ "\x22;");
	%fileObj.writeLine("cash = \x22" @ %cash @ "\x22;");
	%fileObj.writeLine("hasRadio = \x22" @ %hasRadio @ "\x22;");
	%fileObj.writeLine("underStandsHuman = \x22" @ %underStandsHuman @ "\x22;");
	%fileObj.writeLine("underStandsBioderm = \x22" @ %underStandsBioderm @ "\x22;");
	%fileObj.writeLine("underStandsDraakan = \x22" @ %underStandsDraakan @ "\x22;");
	%fileObj.writeLine("underStandsCriollos = \x22" @ %underStandsCriollos @ "\x22;");
	%fileObj.writeLine("");

	//Compile Inventory List
	%slotCount = %player.weaponSlotCount;
	%healthKits = %player.invRepairKit;
	%fileObj.writeLine("[Inventory]");
	%fileObj.writeLine("slotCount = \x22" @ %slotCount @ "\x22;");

	for (%i = 0; %i < %slotCount; %i++)
	{
		%weaponName = %player.weaponSlot[%i];
		%weaponAmmo = eval("%weaponAmmo = %player.inv" @ %weaponName @ "Ammo" @ ";");
		%fileObj.writeLine("slot" @ %i SPC "= \x22" @ %weaponName @ "\x22;");
		%fileObj.writeLine("slot" @ %i  @ "Ammo" SPC "= \x22" @ %weaponAmmo @ "\x22;");
	}

	%fileObj.writeLine("healthKits = \x22" @ %healthKits @ "\x22;");
	%fileObj.detach();
	logEcho(" -- Save File Written for Player:" SPC %this.namebase SPC "--");
	return true;
}

function gameConnection::applySaveFile(%this)
{
	//Compile Main Variable List
	%mission = $CurrentMission;
	%file = "data/game/saves/" @ %mission @ "/" @ %this.guid @ ".txt";

	if (!isFile(%file))
	return false;

	%transform = getBlockData(%file,"Character",1,"transform");
	%velocity = getBlockData(%file,"Character",1,"velocity");
	%damage = getBlockData(%file,"Character",1,"damage");
	%race = getBlockData(%file,"Character",1,"race");
	%armor = getBlockData(%file,"Character",1,"armor");
	%energy = getBlockData(%file,"Character",1,"energyLevel");
	%whiteout = getBlockData(%file,"Character",1,"whiteOut");
	%damageFlash = getBlockData(%file,"Character",1,"damageFlash");
	%cash = getBlockData(%file,"Character",1,"cash");
	%hasRadio = getBlockData(%file,"Character",1,"hasRadio");
	%underStandsHuman = getBlockData(%file,"Character",1,"underStandsHuman");
	%underStandsBioderm = getBlockData(%file,"Character",1,"underStandsBioderm");
	%underStandsDraakan = getBlockData(%file,"Character",1,"underStandsDraakan");
	%underStandsCriollos = getBlockData(%file,"Character",1,"underStandsCriollos");

	%player = %this.player;
	%player.setTransform(%transform);
	%player.setVelocity(%velocity);
	%player.applyDamage(%damage);
	%player.setArmor(%armor);
	%player.setEnergyLevel(%energy);
	%player.setWhiteout(%whiteOut);
	%player.setDamageFlash(%damageFlash);
	%this.cash = %cash;
	%this.underStandsHuman = %underStandsHuman;
	%this.underStandsBioderm = %underStandsBioderm;
	%this.underStandsDraakan = %underStandsDraakan;
	%this.underStandsCriollos = %underStandsCriollos;

	return true;
	for (%i = 0; %i < %slotCount; %i++)
	{
		%weaponName = %player.weaponSlot[%i];
		%weaponAmmo = eval("%weaponAmmo = %player.inv" @ %weaponName @ "Ammo" @ ";");
		%fileObj.writeLine("slot" @ %i SPC "= \x22" @ %weaponName @ "\x22;");
		%fileObj.writeLine("slot" @ %i  @ "Ammo" SPC "= \x22" @ %weaponAmmo @ "\x22;");
	}

	%fileObj.writeLine("healthKits = \x22" @ %healthKits @ "\x22;");
	return;
}

// Generic Import Functions
function importGameData()
{
	importGems();
	importOres();
	importCharacters();
	return true;
}

// Gem Import Functions
function importGems()
{
	if (!IsObject(GemData))
	{
		new ScriptObject(GemData);

		if (!IsObject(GameData))
			new simGroup(GameData);

		GameData.add(GemData);
	}
	else
		return true;

	%file = "data/game/gems.txt";
	%count = getBlockCount(%file,"Gem") + 1;

	for (%i = 1; %i < %count; %i++)
	{
		%name = getBlockData(%file,"Gem",%i,"Name");
		%price = getBlockData(%file,"Gem",%i,"Price");
		%sellPrice = getBlockData(%file,"Gem",%i,"SellPrice");

		GemData.gem[%i] = %name;
		GemData.price[%name] = %price;
		GemData.sellPrice[%name] = %sellPrice;
		warn("Imported gem:" SPC %name);

		GemData.gemCount = %count--;
	}
}

// Ore Import Functions
function importOres()
{
	if (!IsObject(OreData))
	{
		new ScriptObject(OreData);

		if (!IsObject(GameData))
			new simGroup(GameData);

		GameData.add(OreData);
	}
	else
		return true;

	%file = "data/game/ores.txt";
	%count = getBlockCount(%file,"Ore") + 1;

	for (%i = 1; %i < %count; %i++)
	{
		%name = getBlockData(%file,"Ore",%i,"Name");
		%price = getBlockData(%file,"Ore",%i,"Price");
		%sellPrice = getBlockData(%file,"Ore",%i,"SellPrice");

		OreData.ore[%i] = %name;
		OreData.price[%name] = %price;
		OreData.sellPrice[%name] = %sellPrice;
		warn("Imported ore:" SPC %name);
	}
	OreData.oreCount = %count--;
}

// Character Import Functions
function spawnCharacter(%name,%trans,%aimPos,%team)
{
	%object = "Character" @ %name;

	if (!IsObject(%object))
	return false;

	%Bname = %object.name;
	%race = %object.race;
	%skin = %object.skin;
	%voice = %object.voice;
	%voicePitch = %object.voicePitch;
	%sex = %object.sex;

	%bot = aiConnectByName(%Bname,%team);
	%bot.race = %race;
	%bot.skin = addTaggedString(%skin);
	%bot.voice = %voice;
	%bot.voiceTag = addTaggedString(%voice);
	%bot.voicePitch = %voicePitch;
	%bot.sex = %sex;
	setVoice(%bot,%voice, %voicePitch);
	setSkin(%bot,%skin);
	setSkin(%bot,%skin);
	setTeam(%bot, %team);
	%bot.player.setArmor("light");
	%bot.player.setTransform(%trans);
	%bot.aimAt(%aimPos);
	warn("Spawned Character:" SPC %name);
}

function importCharacters()
{
	%path = "data/game/characters/*.txt";
	for( %file = findFirstFile( %path ); %file !$= ""; %file = findNextFile( %path ) )
	{
		%name = getFileNameFromString(%file);
		%pos = strStr(%name,".");
		%character = getSubStr(%name,0,%pos);
		importCharacter(%character);
	}
}

function importCharacter(%character)
{
	%prefix = "data/game/characters/";
	%file = %prefix @ %character @ ".txt";
	%charName = %character;
	%character = strReplace("Character" @ %character," ","_");

	if (!IsFile(%file))
		return false;

	if (!IsObject(%character))
	{
		new scriptObject(%character);
		if (!IsObject(GameData))
			new simGroup(GameData);

		GameData.add(%character);
	}
	else
		return true;

	//Get our variable values ...
	%name = getBlockData(%file,"Character",1,"Name");
	%race = getBlockData(%file,"Character",1,"Race");
	%sex = getBlockData(%file,"Character",1,"Sex");
	%skin = getBlockData(%file,"Character",1,"Skin");
	%voice = getBlockData(%file,"Character",1,"Voice");
	%voicePitch = getBlockData(%file,"Character",1,"VoicePitch");

	//Import Message Arrays ... and assign them
	%arrayName[0] = "Death";
	%arrayName[1] = "Kill";
	%arrayName[2] = "Healed";
	%arrayCount = 3;

	for (%i = 0; %i < %arrayCount; %i++)
	{
		%arrayVariableName[%i] = %arrayName[%i] @ "MessageArray";
		for (%j = 0; %j < 100; %j++)
		{
			%arrayTest = getArrayData(%file,%arrayName[%i],%j);
			if (%arrayTest !$= "}")
			{
				if (%j == 0)
					%arrayData[%i] = %arrayData[%i] @ %arrayTest;
				else
					%arrayData[%i] = %arrayData[%i] @ "\t" @ %arrayTest;
			}
			else
				break;
		}
		eval(%character @ "." @ %arrayVariableName[%i] SPC "= \x22" @ %arrayData[%i] @ "\x22;");
	}
	//Assign the variables now ...
	%character.name = %name;
	%character.race = %race;
	%character.sex = %sex;
	%character.skin = %skin;
	%character.voice = %voice;
	%character.voicePitch = %voicePitch;
	warn("Imported Character:" SPC %charname);
}
