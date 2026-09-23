# R08: Deploy path

## Answer (simplest reliable path)
**One Azure Container App serves both the API and the built frontend.** FastAPI mounts `frontend/dist` with `StaticFiles` at `/`, and the API stays under `/api`. Consequences:
- One deploy command, one URL, and **no CORS** (same origin).
- No Static Web Apps resource, no second pipeline, no SPA routing config beyond a catch-all that returns `index.html`.
- This replaces decision 0001 #11. See decision 0002.

Steps (full list in `tasks/P1-09-azure-setup.md` and P3-04):
```bash
brew install azure-cli && az login
az extension add --name containerapp --upgrade
# multi-stage Dockerfile at repo root: node builds frontend -> python image with uv, copies dist
az containerapp up --name navigator-api --resource-group rg-navigator --location eastus2 \
  --source . --ingress external --target-port 8000 \
  --env-vars APP_MODE=live FOUNDRY_MODEL=... AZURE_SEARCH_INDEX=navigator-kb
```
`az containerapp up --source .` builds in Azure Container Registry, so no local Docker push is needed. Rerunning it redeploys.

- **Secrets:** `az containerapp secret set` plus `--env-vars NAME=secretref:name`. Key Vault is optional. Skip it unless time allows (noted as an upgrade path).
- **Managed identity:** `az containerapp identity assign --system-assigned`, then role assignments on the Foundry resource (R02).
- **Scale:** `--min-replicas 1` during judging, so there's no cold start.
- **Rollback:** `az containerapp revision list` / `az containerapp ingress traffic set --revision-weight <prev>=100`.
- GitHub Actions deploy: optional. The command above is the deploy.

## Evidence
- https://learn.microsoft.com/en-us/azure/container-apps/containerapp-up
- https://learn.microsoft.com/en-us/azure/container-apps/quickstart-code-to-cloud

## Impact
P3-04, ARCHITECTURE.md diagram, decision 0002, `.env.example` (`FRONTEND_ORIGIN` is only needed for local dev CORS).
