# Docker Execution Findings

- Generated at: `2026-04-03T16:42:55+00:00`
- Shared substrate model: `True`
- Networks: `local-network, caldera-kali-network, kali-nginx-network, nginx-db-network`
- Runtime script repairs: `29`
- Generated runtime config files: `.docker/caldera/conf/agents.yml, .docker/caldera/conf/payloads.yml`
- Host architecture patches: `.docker/caldera/Dockerfile, .docker/kali/Dockerfile`
- Operations with progress: `8/8`
- Total successful links: `70`
- Total failed links: `0`
- Total pending links: `6`
- Poll timeout reached: `False`
- Quiescent plateau reached: `True`

## Architecture Findings

- Nginx bootstrap scripts: `8`
- DB bootstrap scripts: `8`
- Both target-side entrypoints load every campaign bootstrap script during container startup, which yields one shared multi-campaign substrate.

## Execution Findings

### OP001 — APT41 DUST
- State: `running`
- Links observed: `10`
- Successful links: `9`
- Failed links: `0`
- Pending links: `1`
- Blocking technique: `T1119` T1119 - Automated Collection

- Non-zero link 10: `T1119` T1119 - Automated Collection -> status `-3`
  command: `curl http://172.21.0.20/crm.php -s --fail --retry 3`
  output: `False`

### OP002 — C0010
- State: `running`
- Links observed: `10`
- Successful links: `9`
- Failed links: `0`
- Pending links: `1`
- Blocking technique: `T1529` END OF C0010

- Non-zero link 10: `T1529` END OF C0010 -> status `-3`
  command: `echo "END OF C0010"`
  output: `False`

### OP003 — C0026
- State: `running`
- Links observed: `7`
- Successful links: `7`
- Failed links: `0`
- Pending links: `0`
- Blocking technique: `T1529` END OF C0026

### OP004 — CostaRicto
- State: `running`
- Links observed: `10`
- Successful links: `9`
- Failed links: `0`
- Pending links: `1`
- Blocking technique: `T1572` T1572 - Protocol Tunneling

- Non-zero link 10: `T1572` T1572 - Protocol Tunneling -> status `-3`
  command: `fuser -k 2222/tcp 2>/dev/null; sshpass -p 'RootPass123' ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -L 2222:172.22.0.20:22 root@172.21.0.20 -N & TUNNEL_PID=$!; sleep 5; sshpass -p 'RootPass123' ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null root@localhost -p 2222 id; kill $TUNNEL_PID`
  output: `False`

### OP005 — Operation MidnightEclipse
- State: `running`
- Links observed: `10`
- Successful links: `9`
- Failed links: `0`
- Pending links: `1`
- Blocking technique: `T1584.003` T1584.003 - Virtual Private Server

- Non-zero link 10: `T1584.003` T1584.003 - Virtual Private Server -> status `-3`
  command: `sshpass -p RootPass123 ssh -o StrictHostKeyChecking=no root@172.21.0.20 'id && cat /etc/passwd' && sshpass -p RootPass123 ssh -o StrictHostKeyChecking=no root@172.21.0.20 'sshpass -p RootPass123 ssh -o StrictHostKeyChecking=no root@172.22.0.20 id'`
  output: `False`

### OP006 — Outer Space
- State: `running`
- Links observed: `9`
- Successful links: `9`
- Failed links: `0`
- Pending links: `0`
- Blocking technique: `T1529` END OF OUTER SPACE

### OP007 — Salesforce Data Exfiltration
- State: `running`
- Links observed: `10`
- Successful links: `9`
- Failed links: `0`
- Pending links: `1`
- Blocking technique: `T1083` T1083 - File and Directory Discovery

- Non-zero link 10: `T1083` T1083 - File and Directory Discovery -> status `-3`
  command: `sshpass -p 'RootPass123' ssh root@172.21.0.20 'ls -la / && find / -maxdepth 2 -type d'`
  output: `False`

### OP008 — ShadowRay
- State: `running`
- Links observed: `10`
- Successful links: `9`
- Failed links: `0`
- Pending links: `1`
- Blocking technique: `T1496.001` T1496.001 - Compute Hijacking

- Non-zero link 10: `T1496.001` T1496.001 - Compute Hijacking -> status `-3`
  command: `echo 'mining crypto'`
  output: `False`

## Paper Takeaways

- The Docker artifact executes all curated campaigns inside one shared pre-composed substrate, not one isolated SUT per campaign.
- For this legacy Caldera path, executed work is visible in operation.chain even when operation.steps remains empty.
- Reproducibility depends on runtime repair outside the frozen artifact: missing executable bits, missing Caldera conf files, and host-aware bootstrap adjustments are required for clean replay on a fresh ARM64 host.
- All curated campaigns progressed. 0 record at least one non-zero link status, 6 still have a pending tail under the observed window, and 3 reach explicit end markers.
- The legacy artifact demonstrates partial procedural enactment on a shared laboratory environment, not independent push-button replay of fully isolated campaigns.
