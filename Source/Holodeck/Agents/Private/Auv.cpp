// MIT License (c) 2019 BYU PCCL see LICENSE file

#include "Holodeck.h"
#include "Auv.h"


// Sets default values
AAuv::AAuv() {
	PrimaryActorTick.bCanEverTick = true;

	// Set the defualt controller
	AIControllerClass = LoadClass<AController>(NULL, TEXT("/Script/Holodeck.AuvController"), NULL, LOAD_None, NULL);
	AutoPossessAI = EAutoPossessAI::PlacedInWorld;
}

void AAuv::InitializeAgent() {
	Super::InitializeAgent();
	RootMesh = Cast<UStaticMeshComponent>(RootComponent);
}

// Called every frame
void AAuv::Tick(float DeltaSeconds) {
	Super::Tick(DeltaSeconds);
	//if (GEngine)
	//	GEngine->AddOnScreenDebugMessage(-1, 15.0f, FColor::Red, FString::Printf(TEXT("Command %f %f %f %f"), CommandArray[0], CommandArray[1], CommandArray[2], CommandArray[3]));
	
	//Pull everything we need from the actor once
	float Mass = RootMesh->GetMass();
	FVector ActorLocation = GetActorLocation();
	FRotator ActorRotation = GetActorRotation();

	// Get and apply Bouyant Force
	float BouyantForce = volume * gravity * water_density;
	FVector BouyantVector = FVector(0, 0, BouyantForce);
	BouyantVector = ConvertLinearVector(BouyantVector, ClientToUE);

	FVector COB_World = ActorLocation + ActorRotation.RotateVector(COBLocation);
	RootMesh->AddForceAtLocation(BouyantVector, COB_World);

	// Make sure we're within limits
	float UpValue = FMath::Clamp(CommandArray[0], MIN_ACCEL, MAX_ACCEL);
	float DownValue = FMath::Clamp(CommandArray[1], MIN_ACCEL, MAX_ACCEL);
	float LeftValue = FMath::Clamp(CommandArray[2], MIN_ACCEL, MAX_ACCEL);
	float RightValue = FMath::Clamp(CommandArray[3], MIN_ACCEL, MAX_ACCEL);

	// Convert all thrusters
	FVector UpThruster = ConvertLinearVector(FVector(UpValue*Mass, 0, 0), ClientToUE);
	FVector DownThruster = ConvertLinearVector(FVector(DownValue*Mass, 0, 0), ClientToUE);
	FVector LeftThruster = ConvertLinearVector(FVector(LeftValue*Mass, 0, 0), ClientToUE);
	FVector RightThruster = ConvertLinearVector(FVector(RightValue*Mass, 0, 0), ClientToUE);

	// Get Location of Thrusters
	FVector UpThruster_World = ActorLocation + ActorRotation.RotateVector(UpThrusterLocation);
	FVector DownThruster_World = ActorLocation + ActorRotation.RotateVector(DownThrusterLocation);
	FVector LeftThruster_World = ActorLocation + ActorRotation.RotateVector(LeftThrusterLocation);
	FVector RightThruster_World = ActorLocation + ActorRotation.RotateVector(RightThrusterLocation);

	// Apply Thrusters
	RootMesh->AddForceAtLocation(ActorRotation.RotateVector(UpThruster), UpThruster_World);
	RootMesh->AddForceAtLocation(ActorRotation.RotateVector(DownThruster), DownThruster_World);
	RootMesh->AddForceAtLocation(ActorRotation.RotateVector(LeftThruster), LeftThruster_World);
	RootMesh->AddForceAtLocation(ActorRotation.RotateVector(RightThruster), RightThruster_World);

	// If the turtle is upside down it is abused
	if (this->GetActorUpVector().Z < -0.5) {
		this->IsAbused = true;
	}
}



