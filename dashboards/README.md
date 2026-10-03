# Host both dashboards from your class repository

Use your existing GitHub fork of the class repository. You need permission to push changes to that fork. Both apps live in the same repository but run as two separate Render **Web Services**, each with its own URL.

```text
dashboards/
    README.md
    class-demo/
        app.py
        requirements.txt
        data/
            cpsc_neiss_school_age_micromobility_2025.csv
            README.md
    personal/
        app.py
        requirements.txt
        data/
            README.md
            [your dataset goes here]
```

## First: deploy the in-class bike/scooter demo

### Save and update your class fork using VS Code

Use the installed **GitHub Pull Requests and Issues** extension for GitHub sign-in and VS Code's **Source Control** view for Git operations. No terminal commands are needed. Updating has two parts: bring the instructor's updates into your GitHub fork, then download them into your local folder.

1. In **JupyterLab**, save each notebook you edited, then close its tab so an older open copy cannot overwrite the updated file later.
2. In **VS Code**, choose **File → Open Folder** and open the local folder where you cloned your own class fork. Check the branch name in the lower-left corner; use your assigned course branch. If prompted, sign in to GitHub using the same account that owns your fork.
3. Select **Source Control** in the left sidebar. Review the files listed under **Changes**. Click the **+** beside each file you want to save to stage it. Enter a message such as `Save my lecture work`, then click **Commit**. If no files have changed, skip this step.
4. Open the Command Palette (`Ctrl+Shift+P` on Windows or `Cmd+Shift+P` on macOS), run **Git: Push**, and choose **origin** if asked. This sends your saved commits to your fork. Resolve any reported push problem before continuing; do not force-push or discard your work.
5. Open **your fork on GitHub in a browser**. Confirm that the repository owner is your username and select the same course branch. Click **Sync fork → Update branch** to bring in the instructor's updates. This browser step updates your fork from the course repository; VS Code's **Sync Changes** button alone does not do that. If GitHub reports conflicts, ask the instructor for help rather than choosing an option that discards your commits.
6. Return to VS Code. Open the Command Palette and run **Git: Pull** (choose **origin** and your course branch if prompted). This downloads the updated fork into your local folder. If a merge conflict appears, stop and ask for help before reopening or editing the notebook.
7. In VS Code's **Explorer**, expand **dashboards → class-demo** and confirm that `app.py`, `requirements.txt`, and the dataset under `data` are present. Refresh your fork's GitHub page and check the same files there. Use this repository and branch when connecting Render. Reopen the updated notebook from disk in JupyterLab.

Reference: [VS Code's GitHub integration](https://code.visualstudio.com/docs/sourcecontrol/github) and [Git operations](https://code.visualstudio.com/docs/sourcecontrol/repos-remotes).

1. Save any notebook work and sync your class fork with the course updates. Pull the changes into your local checkout. Confirm that `dashboards/class-demo` appears in your own GitHub repository and selected branch.
2. The class-demo app is ready to run. It contains the four lecture views, an age filter, blue/green/orange/purple device colors, and the additional-care table. You may customize it by replacing `build_dashboard` and its imports with your checked lecture version. Keep the data-loading lines, `app`, and `server` at the bottom.
3. In [Render](https://dashboard.render.com/), connect your GitHub account and select **New → Web Service**. Select your own class fork and the branch containing your dashboard files.
4. Give the service a unique name, such as `yourname-class-demo`, and choose the settings below. The root directory is relative to the GitHub repository root; do not add a leading slash.
5. Deploy. Wait for the service to become live, then open its `onrender.com` URL. Test the age slider and compare the unfiltered totals with the lecture: 6,212 cases and 525 requiring additional care. Keep the source and limitations visible.

| Setting | Class demo | Personal dashboard |
| --- | --- | --- |
| Service type | Web Service | Web Service |
| Repository | Your class fork | The same class fork |
| Branch | Your course branch containing these files | The branch containing your personal app |
| Root Directory | `dashboards/class-demo` | `dashboards/personal` |
| Language | Python | Python |
| Build Command | `pip install -r requirements.txt` | Same |
| Start Command | `gunicorn app:server --bind 0.0.0.0:$PORT` | Same |
| Instance type | Free | Free |

These root directories apply to the student course repositories. In the instructor's canonical source repository only, they begin with `source/dashboards/` instead.

## Then: prepare and deploy your personal dashboard

1. Complete and check the static analysis and dashboard in the lab notebook.
2. Copy the original dataset into `dashboards/personal/data/` and document it in that folder's README. Every supporting file must be inside `personal`; Render cannot access files outside the service root.
3. Open `dashboards/personal/app.py`. Replace its placeholder `build_dashboard(data)` with your complete function and add its imports. Replace `data = None` with the appropriate data-loading statement, following the commented example. Your function should prepare a copy of the original data just as it does in the notebook.
4. Add any additional imported packages to `requirements.txt`. Do not paste notebook `%pip` commands, displayed output, or the notebook launch cell into `app.py`. Keep the supplied `app`, `server`, and guarded local launch lines. The initial starter page only confirms the deployment works; it is not the completed assignment.
5. Commit and push the app, requirements, and dataset to your class fork. Create a **second** Render Web Service from that same repository, using the personal settings above and a distinct service name. Keep the class-demo service.
6. Open the personal URL. Compare all four views with the static analysis and test the controls and empty selections. Submit both public URLs, plus your notebook and code as instructed.

## Updating and testing

Continue analysis in Jupyter. After revising the notebook function, copy the updated function and imports into the corresponding `app.py`, then commit and push. With automatic deployment enabled, changes within each service's root directory redeploy that service. Running a notebook alone does not update Render.

For an optional local deployment check, open a terminal in the app's folder, install its app packages (`pip install dash plotly pandas`, plus any preparation dependencies), then run `python app.py`. The demo uses port 8054; the personal app uses 8055. Stop any notebook app using that same port first. Gunicorn is for Render's Linux environment; it is not needed for this local Windows check.

If deployment fails, inspect Render's logs. Check the root directory, exact filename capitalization, package list, and `server = app.server`. A missing data file often means it was not committed or is outside the app folder. The public URL is shareable; a local `127.0.0.1` URL is not.

## Free service behavior

Each free service sleeps after 15 minutes without traffic and typically takes about a minute to restart. Open both links before a presentation. The workspace shares 750 free running hours per calendar month across services, and other usage limits apply. No database or paid instance is needed for these fixed-file examples. Review current plan limits before deploying.

Official references: [multiple apps in one repository](https://render.com/docs/monorepo-support), [web service setup](https://render.com/docs/web-services), and [free service limits](https://render.com/docs/free).
