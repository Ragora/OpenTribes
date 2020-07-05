//------------------------------------------------------------------------------
// serverRequestHandler.cs
// Server Request Handler
// Copyright (c) 2012 The DarkDragonDX
//==============================================================================

function InteractWithObject(%val)
{
}

function IcreaseRadioFrequency(%val)
{
}

function DecreaseRadioFrequency(%val)
{
}

//These are just here.. just in case.
function OnLANPasswordInput()
{
return 1;
}

function OnLANNameInput()
{
return 1;
}

function clientCmdSetScoreText(%text)
{
 ScoreParent.settext(%text);
 return 1;
}


function alxMusicFadeout(%startvol)
{
%startvol = %startvol - 0.1;

 if (%startvol <= 0)
 {
  alxstopmusic();
  alxsetmusicvolume($pref::audio::musicvolume);
  return;
 }
alxsetmusicvolume(%startvol);
schedule(500,0,"alxmusicfadeout",%startvol);
return 1;
}

function alxMusicFadein(%startvol)
{
%startvol = %startvol + 0.1;

 if (%startvol > 1)
 {
  alxsetmusicvolume($pref::audio::musicvolume);
  return;
 }
alxsetmusicvolume(%startvol);
schedule(500,0,"alxmusicfadein",%startvol);
return 1;
}


function clientCmdAlxMusicFadeout()
{
 alxmusicfadeout($pref::audio::musicvolume);
 return 1;
}

function alxSetMusicVolume(%vol)
{
OP_MusicVolumeSlider.setvalue(%vol);
return %vol;
}



function reLightMission() {
	if ($SceneLighting::lightingProgress == 0 || $SceneLighting::lightingProgress == 1)
		lightScene("",forceAlways);
}

function clientCmdReLightMission() {
	if (!$pref::disallowRelight)
		reLightMission();
}

// -----------------------------------------------------
// Client Hook
// -----------------------------------------------------
package clientMod{
function DispatchLaunchMode()
{
parent::DispatchLaunchMode();

    // check T2 command line arguments
    for(%i = 1; %i < $Game::argc ; %i++)
    {
        %arg = $Game::argv[%i];
        %nextArg = $Game::argv[%i+1];
        %hasNextArg = $Game::argc - %i > 1;

        if( !stricmp(%arg, "-CleanDSO")) //Remove DSO's on shutdown
        {
            $CleanDSO = true;
        }
}
}

function Disconnect()
{
parent::Disconnect();

   //Play the menu audio
   alxplaymusic("T2BOL/Music/Menu.mp3");
   alxMusicFadein(0);
   //Fix the score menu
   ScoreParent.settext("SCORE");
   //Enable continue
   DB_ContinueBTN.setActive(1);
   //Show other elements
    clockHud.setVisible(1);
    timeHud.setVisible(0);
return 1;
}

function OptionsDLG::OnSleep(%this)
{
parent::OnSleep(%this);

 if ($pref::Audio::musicEnabled && !IsObject(ServerConnection))
 {
 alxplaymusic("T2BOL/Music/Menu.mp3");
 alxMusicFadein(0);
 }
}

function GuiMLTextCtrl::onURL(%this, %url)
{
%url = strReplace(%url,"-","\t"); //Reading from files causes some funny issues..

    switch$( getField(%url, 0) )
    {
        case "select":
           %cb = getField(%url, 1);

             if(%cb $= "")
                return;

            %i = 0;
            while((%p[%i] = getField(%url, %i + 2)) !$= "")
                %i++;

        RPG_Category.setText(%cb); //Set the dropdown Text
        RPG_BrowserPane.refresh(); //Force a refresh

        for (%i = 0; %i < RPG_ItemList.rowCount(); %i++)
        {
         %text = RPG_ItemList.getRowText(%i);

          if (%text $= %p0)
          {
           RPG_ItemList.setSelectedRow(%i);
           break; //Tell the for loop to stop and continue executing
          }
        }
        //Now make our category select the correct row
        for (%i =  0; %i < RPG_Category.count; %i++)
        {
         %text = RPG_Category.getTextByID(%i);
          if (%text $= %cb)
          {
           RPG_Category.setSelected(%i);
           return;
          }
        }

         case "call": //Dunno if anybody will use this..
           %cb = getField(%url, 1);

             if(%cb $= "")
                return;

            %i = 0;
            while((%p[%i] = getField(%url, %i + 2)) !$= "")
                %i++;

            call(%cb, %p0, %p1, %p2, %p3, %p4);

         case "input": //Should only be used on the PDA.
           %cb = getField(%url, 1);

             if(%cb $= "")
                return;

            %i = 0;
            while((%p[%i] = getField(%url, %i + 2)) !$= "")
                %i++;

            //%cb is our data type
            //%p0 is the text that shows up above the input box
            //%p1 is the text for the box itself
            InputText.setText(%p0);
            InputTransFrame.setText(%p1);
            Input.setValue("");
            canvas.pushDialog(InputDLG);
            $InputType = %cb;

        default:
            Parent::onURL(%this, %url);
    }
    return;
}
};
activatePackage(clientMod);
