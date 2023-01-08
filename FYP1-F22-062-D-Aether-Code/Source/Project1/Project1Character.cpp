// Copyright Epic Games, Inc. All Rights Reserved.

#include "Project1Character.h"

#include "CustomizableActor.h"
#include "Project1Projectile.h"
#include "Animation/AnimInstance.h"
#include "Camera/CameraComponent.h"
#include "Components/CapsuleComponent.h"
#include "Components/InputComponent.h"
#include "GameFramework/InputSettings.h"

#include "Widgets/Text/ISlateEditableTextWidget.h"


//////////////////////////////////////////////////////////////////////////
// AProject1Character

AProject1Character::AProject1Character()
{
	// Set size for collision capsule
	GetCapsuleComponent()->InitCapsuleSize(55.f, 96.0f);

	// set our turn rates for input
	TurnRateGamepad = 45.f;

	// Create a CameraComponent	
	FirstPersonCameraComponent = CreateDefaultSubobject<UCameraComponent>(TEXT("FirstPersonCamera"));
	FirstPersonCameraComponent->SetupAttachment(GetCapsuleComponent());
	FirstPersonCameraComponent->SetRelativeLocation(FVector(-39.56f, 1.75f, 64.f)); // Position the camera
	FirstPersonCameraComponent->bUsePawnControlRotation = true;

	// Create a mesh component that will be used when being viewed from a '1st person' view (when controlling this pawn)
	Mesh1P = CreateDefaultSubobject<USkeletalMeshComponent>(TEXT("CharacterMesh1P"));
	Mesh1P->SetOnlyOwnerSee(true);
	Mesh1P->SetupAttachment(FirstPersonCameraComponent);
	Mesh1P->bCastDynamicShadow = false;
	Mesh1P->CastShadow = false;
	Mesh1P->SetRelativeRotation(FRotator(1.9f, -19.19f, 5.2f));
	Mesh1P->SetRelativeLocation(FVector(-0.5f, -4.4f, -155.7f));

}

void AProject1Character::BeginPlay()
{
	// Call the base class  
	Super::BeginPlay();

}

//////////////////////////////////////////////////////////////////////////// Input

void AProject1Character::SetupPlayerInputComponent(class UInputComponent* PlayerInputComponent)
{
	// Set up gameplay key bindings
	check(PlayerInputComponent);

	PlayerInputComponent->BindAction("Interact", IE_Pressed,this, &AProject1Character::SpawnAsset);
	// Bind jump events
	PlayerInputComponent->BindAction("Jump", IE_Pressed, this, &ACharacter::Jump);
	PlayerInputComponent->BindAction("Jump", IE_Released, this, &ACharacter::StopJumping);

	// Bind fire event
	PlayerInputComponent->BindAction("PrimaryAction", IE_Pressed, this, &AProject1Character::OnPrimaryAction);

	// Enable touchscreen input
	EnableTouchscreenMovement(PlayerInputComponent);

	// Bind movement events
	PlayerInputComponent->BindAxis("Move Forward / Backward", this, &AProject1Character::MoveForward);
	PlayerInputComponent->BindAxis("Move Right / Left", this, &AProject1Character::MoveRight);

	// We have 2 versions of the rotation bindings to handle different kinds of devices differently
	// "Mouse" versions handle devices that provide an absolute delta, such as a mouse.
	// "Gamepad" versions are for devices that we choose to treat as a rate of change, such as an analog joystick
	PlayerInputComponent->BindAxis("Turn Right / Left Mouse", this, &APawn::AddControllerYawInput);
	PlayerInputComponent->BindAxis("Look Up / Down Mouse", this, &APawn::AddControllerPitchInput);
	PlayerInputComponent->BindAxis("Turn Right / Left Gamepad", this, &AProject1Character::TurnAtRate);
	PlayerInputComponent->BindAxis("Look Up / Down Gamepad", this, &AProject1Character::LookUpAtRate);
}

void AProject1Character::OnPrimaryAction()
{
	// Trigger the OnItemUsed Event
	OnUseItem.Broadcast();
}

void AProject1Character::BeginTouch(const ETouchIndex::Type FingerIndex, const FVector Location)
{
	if (TouchItem.bIsPressed == true)
	{
		return;
	}
	if ((FingerIndex == TouchItem.FingerIndex) && (TouchItem.bMoved == false))
	{
		OnPrimaryAction();
	}
	TouchItem.bIsPressed = true;
	TouchItem.FingerIndex = FingerIndex;
	TouchItem.Location = Location;
	TouchItem.bMoved = false;
}

void AProject1Character::EndTouch(const ETouchIndex::Type FingerIndex, const FVector Location)
{
	if (TouchItem.bIsPressed == false)
	{
		return;
	}
	TouchItem.bIsPressed = false;
}

void AProject1Character::MoveForward(float Value)
{
	if (Value != 0.0f)
	{
		// add movement in that direction
		AddMovementInput(GetActorForwardVector(), Value);
	}
}

void AProject1Character::MoveRight(float Value)
{
	if (Value != 0.0f)
	{
		// add movement in that direction
		AddMovementInput(GetActorRightVector(), Value);
	}
}

void AProject1Character::TurnAtRate(float Rate)
{
	// calculate delta for this frame from the rate information
	AddControllerYawInput(Rate * TurnRateGamepad * GetWorld()->GetDeltaSeconds());
}

void AProject1Character::LookUpAtRate(float Rate)
{
	// calculate delta for this frame from the rate information
	AddControllerPitchInput(Rate * TurnRateGamepad * GetWorld()->GetDeltaSeconds());
}

bool AProject1Character::EnableTouchscreenMovement(class UInputComponent* PlayerInputComponent)
{
	if (FPlatformMisc::SupportsTouchInput() || GetDefault<UInputSettings>()->bUseMouseForTouch)
	{
		PlayerInputComponent->BindTouch(EInputEvent::IE_Pressed, this, &AProject1Character::BeginTouch);
		PlayerInputComponent->BindTouch(EInputEvent::IE_Released, this, &AProject1Character::EndTouch);

		return true;
	}
	
	return false;
}

void AProject1Character::SpawnAsset()
{
	GEngine->Exec(NULL, TEXT("python3 -m pip install -U matplotlib"));

	GEngine->Exec(NULL, TEXT("python3 /home/aim2/Documents/complete_py_pipeline.py"));
	UE_LOG(LogTemp, Warning, TEXT("INSIDE FTN 2.0"));
	// FString result = UUnrealEnginePython::ExecutePythonScript("print('Hello, World!')");
	// UE_LOG(LogTemp, Warning, TEXT("%s"), *result);
	
	FVector SpawnLocation = this->GetActorLocation()+ this->GetActorForwardVector() * 500.0f;
	FRotator SpawnRotation = FRotator(0.0, 0.0,0.0);

	
	
	ACustomizableActor* actor = (ACustomizableActor*) GetWorld()->SpawnActor(ACustomizableActor::StaticClass(),&SpawnLocation, &SpawnRotation);
	//ObjectToMove->SetActorLocation(CharacterLocation + CharacterForwardVector * 100.0f);

	FVector ActorLocation = actor->GetActorLocation();
	
	float groundHeight = GetGroundHeightAtLocation(ActorLocation);
	actor->SetActorLocation(FVector(ActorLocation.X, ActorLocation.Y, groundHeight));
	
	FString AssetPath = "/Game/Megascans/3D_Assets/Mossy_Forest_Boulder_we2rbizaw/S_Mossy_Forest_Boulder_we2rbizaw_lod3_Var1.S_Mossy_Forest_Boulder_we2rbizaw_lod3_Var1";
	actor->SetStaticMesh(AssetPath);
}

float AProject1Character::GetGroundHeightAtLocation(const FVector& Location)
{
	FHitResult HitResult;
	FCollisionQueryParams QueryParams = FCollisionQueryParams("GetGroundHeight", true, NULL);
	QueryParams.bReturnPhysicalMaterial = true;
	bool bHit = this->GetWorld()->LineTraceSingleByChannel(HitResult, Location, FVector(Location.X, Location.Y, Location.Z - 10000.0f), ECC_WorldDynamic, QueryParams);
	
	if (bHit)
	{
		return HitResult.ImpactPoint.Z;
	}
	else
	{
		return 0.0f;
	}
}