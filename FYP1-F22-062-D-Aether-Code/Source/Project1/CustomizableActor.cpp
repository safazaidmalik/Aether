// Fill out your copyright notice in the Description page of Project Settings. 
  
  
 #include "CustomizableActor.h" 
  
 #include "ShaderCompiler.h" 
 #include "Kismet/GameplayStatics.h" 
  
  
 // Sets default values 
 ACustomizableActor::ACustomizableActor() { 
         // Set this actor to call Tick() every frame.  You can turn this off to improve performance if you don't need it. 
         PrimaryActorTick.bCanEverTick = true; 
  
         MyMesh = CreateDefaultSubobject<UStaticMeshComponent>(TEXT("/Game/StarterContent/Shapes/Shape_Cube.Shape_Cube")); 
         MyMesh->SetupAttachment(RootComponent); 
         RootComponent = MyMesh; 
  
  
 } 
  
 template <typename ObjClass> 
 static FORCEINLINE ObjClass* LoadObjFromPath(const FName& Path) { 
         if (Path == NAME_None) return nullptr; 
  
         return Cast<ObjClass>(StaticLoadObject(ObjClass::StaticClass(), nullptr, *Path.ToString())); 
 } 
  
 static FORCEINLINE UMaterialInterface* LoadMaterialFromPath(const FName& Path) { 
         if (Path == NAME_None) return nullptr; 
  
         return LoadObjFromPath<UMaterialInterface>(Path); 
 } 
  
  
 // Called when the game starts or when spawned 
 void ACustomizableActor::BeginPlay() { 
         Super::BeginPlay(); 
 } 
  
  
 void ACustomizableActor::SetMaterial(FString path) { 
         ActorMaterial = LoadMaterialFromPath(FName(*path)); 
  
         UMaterialInstanceDynamic* DynamicMeterial = UMaterialInstanceDynamic::Create(ActorMaterial, this); 
  
         MyMesh->SetMaterial(0, DynamicMeterial); 
  
 } 
  
 void ACustomizableActor::SetStaticMesh(FString path) { 
         UStaticMesh* meshToUse = Cast<UStaticMesh>(StaticLoadObject(UStaticMesh::StaticClass(), NULL, *path)); 
  
         if (meshToUse && MyMesh) { 
                 MyMesh->SetStaticMesh(meshToUse); 
         } 
 } 
  
 FString ACustomizableActor::GetActorName() { 
         return ActorName; 
 } 
  
 void ACustomizableActor::SetActorName(FString name) { 
         ActorName = name; 
 } 
  
  
 // Called every frame 
 void ACustomizableActor::Tick(float DeltaTime) { 
         Super::Tick(DeltaTime); 
  
 } 
  
 void ACustomizableActor::MoveActor(FVector Location) { 
         SetActorLocation(GetActorLocation() + Location); 
 } 
  
 UStaticMeshComponent* ACustomizableActor::GetStaticMesh() { 
         return MyMesh; 
 } 
  
 void ACustomizableActor::RotateActor(FRotator Rotation) { 
         SetActorRotation(GetActorRotation() + Rotation); 
 } 
  
 void ACustomizableActor::DeleteAllCustomizableActors() { 
         TArray<AActor*> FoundActors; 
         UWorld* world = GEngine->GameViewport-> 
                                  GetWorld(); 
         UGameplayStatics::GetAllActorsOfClass(world, StaticClass(), FoundActors); 
  
         for (AActor* Actor : FoundActors) { 
                 Actor->Destroy(); 
         } 
 }