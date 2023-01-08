// Copyright Epic Games, Inc. All Rights Reserved.

#include "Project1GameMode.h"
#include "Project1Character.h"
#include "UObject/ConstructorHelpers.h"

AProject1GameMode::AProject1GameMode()
	: Super()
{
	// set default pawn class to our Blueprinted character
	static ConstructorHelpers::FClassFinder<APawn> PlayerPawnClassFinder(TEXT("/Game/FirstPerson/Blueprints/BP_FirstPersonCharacter"));
	DefaultPawnClass = PlayerPawnClassFinder.Class;

}
