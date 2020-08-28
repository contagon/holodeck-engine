// MIT License (c) 2019 BYU PCCL see LICENSE file

#pragma once

#include "GameFramework/Pawn.h"
#include "HolodeckAgent.h"
#include "Auv.generated.h"

static constexpr float MAX_ACCEL = 3.0f;
static constexpr float MIN_ACCEL = 0.0f;

UCLASS()
/**
* AAuv
* Inherits from the HolodeckAgent class
* On any tick this object will apply the given forces.
* Desired values must be set by a controller.
*/
class HOLODECK_API AAuv : public AHolodeckAgent
{
	GENERATED_BODY()

public:
	/**
	* Default Constructor.
	*/
	AAuv();

	void InitializeAgent() override;

	/**
	* Tick
	* Called each frame.
	* @param DeltaSeconds the time since the last tick.
	*/
	void Tick(float DeltaSeconds) override;

	UPROPERTY(BlueprintReadWrite, Category = UAVMesh)
		UStaticMeshComponent* RootMesh;

	unsigned int GetRawActionSizeInBytes() const override { return 4 * sizeof(float); };
	void* GetRawActionBuffer() const override { return (void*)CommandArray; };

	// Allows agent to fall up to ~8 meters
	float GetAccelerationLimit() override { return 400; }

	// Constants
	const float volume = 2;
	const float water_density = 997;
	const float gravity = 9.81;

	// Location of things
	const FVector COBLocation = FVector(0, 0, 5);
	const FVector LeftThrusterLocation = FVector(-100, -25, 5);
	const FVector RightThrusterLocation = FVector(-100, 25, 5);
	const FVector DownThrusterLocation = FVector(-100, 0, -20);
	const FVector UpThrusterLocation = FVector(-100, 0, 30);

private:
	/**
	* 0: UpThruster
	* 1: DownThruster
	* 2: LeftThruster
	* 3: RightThruster
	*/
	float CommandArray[4];

};
