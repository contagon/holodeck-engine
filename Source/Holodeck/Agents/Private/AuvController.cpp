// MIT License (c) 2019 BYU PCCL see LICENSE file

#include "Holodeck.h"
#include "AuvController.h"

AAuvController::AAuvController(const FObjectInitializer& ObjectInitializer)
	: AHolodeckPawnController(ObjectInitializer) {
	UE_LOG(LogTemp, Warning, TEXT("Auv Controller Initialized"));
}

AAuvController::~AAuvController() {}
