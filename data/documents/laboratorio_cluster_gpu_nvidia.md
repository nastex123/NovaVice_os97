# Universidad Tecnológica de Vanguardia (Nova Tech University)
## Normativa y Guía de Uso: Clúster de Supercómputo GPU NVIDIA H100

### 1. Infraestructura del Clúster
Nova Tech University cuenta con el clúster *Nova Titan Cluster*, equipado con 64 GPUs NVIDIA H100 Tensor Core de 80GB interconectadas mediante NVIDIA Quantum-2 InfiniBand a 400 Gbps.

### 2. Políticas de Acceso y Asignación de Cuotas
- **Estudiantes de Grado:** Asignación automática de 50 horas mensuales de GPU para asignaturas de IA y Deep Learning.
- **Estudiantes de Tesis y Posgrado:** Asignación ampliada de hasta 200 horas mensuales previa solicitud del tutor docente.
- **Gestor de Trabajos:** La programación de tareas se gestiona mediante el orquestador Slurm (`sbatch`, `squeue`, `scancel`).