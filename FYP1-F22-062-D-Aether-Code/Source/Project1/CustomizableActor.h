// Fill out your copyright notice in the Description page of Project Settings. 
  
#pragma once 
  
#include "CoreMinimal.h" 
#include "GameFramework/Actor.h" 
#include "CustomizableActor.generated.h" 
  
UCLASS() 
class PROJECT1_API ACustomizableActor : public AActor { 
	GENERATED_BODY() 
  
	UPROPERTY(EditAnywhere) 
	FString ActorName; 
          
public: 
	// Sets default values for this actor's properties 
	ACustomizableActor(); 
	UFUNCTION(BlueprintCallable) 
	FString GetActorName(); 
	void SetActorName(FString Name); 
  
protected: 
	// Called when the game starts or when spawned 
	virtual void BeginPlay() override; 
  
	UPROPERTY(VisibleAnywhere) 
	class UStaticMeshComponent* MyMesh; 
  
  
	UPROPERTY(EditAnywhere) 
	class UMaterialInterface* ActorMaterial; 
  
  
  
public: 
	// Called every frame 
  
	virtual void Tick(float DeltaTime) override; 
  
	UFUNCTION(BlueprintCallable) 
	void SetMaterial(FString path); 
  
	UFUNCTION(BlueprintCallable) 
	void SetStaticMesh(FString path); 
  
	UFUNCTION(BlueprintCallable) 
	UStaticMeshComponent* GetStaticMesh(); 
  
	void MoveActor(FVector Location); 
  
	void RotateActor(FRotator Rotation); 
  
	static void DeleteAllCustomizableActors(); 
  
};