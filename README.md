# ROKEY_high
DOOSAN ROKEY 심화반 스타벅스 프로젝트

```mermaid
graph TD;
    A[MainWindow] --> B[FindMyCarInfoScreen]
    A --> C[SelectMyCarInfoScreen]
    A --> D[BarcodeScannerApp]
    A --> E[PaymentScreen]
    A --> F[ExitScreen]
    
    B -->|입력된 차량 번호| C
    C -->|선택된 차량 정보| D
    D -->|인식된 바코드 정보| E
    E -->|결제 완료| F
    
    subgraph Styles
        G[SBUCKStyle] --> B
        G --> C
        G --> D
        G --> E
        G --> F
    end
    
    subgraph Barcode
        H[BarcodeScannerWorker] --> D
    end
```