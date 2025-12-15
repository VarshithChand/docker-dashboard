from flask import Flask, render_template, request, redirect, url_for, flash
import subprocess

app = Flask(__name__)
app.secret_key = "docker_secret_key"


def run_cmd(cmd):
    return subprocess.getoutput(cmd)


# ---------- HELPERS ----------

def container_status(name):
    """
    Returns: running | exited | not_found
    """
    out = run_cmd("docker ps -a --format '{{.Names}}|{{.Status}}'")
    if not out:
        return "not_found"

    for line in out.splitlines():
        parts = line.split("|")
        if len(parts) != 2:
            continue
        cname, status = parts
        if cname == name:
            return "running" if "Up" in status else "exited"

    return "not_found"


# ---------- SAFE DATA FUNCTIONS ----------

def get_containers():
    out = run_cmd("docker ps -a --format '{{.Names}}|{{.Image}}|{{.Status}}'")
    containers = []

    if not out:
        return containers

    for line in out.splitlines():
        parts = line.split("|")
        if len(parts) != 3:
            continue

        name, image, status = parts
        containers.append({
            "name": name.strip(),
            "image": image.strip(),
            "status": status.strip(),
            "stopped": "Exited" in status
        })

    return containers


def get_images():
    out = run_cmd("docker images --format '{{.Repository}}:{{.Tag}}|{{.ID}}'")
    images = []

    if not out:
        return images

    for line in out.splitlines():
        parts = line.split("|")
        if len(parts) != 2:
            continue

        repo, iid = parts
        images.append({
            "repo": repo.strip(),
            "id": iid.strip()
        })

    return images


def get_volumes():
    out = run_cmd("docker volume ls --format '{{.Name}}'")
    return out.splitlines() if out else []


def get_networks():
    out = run_cmd("docker network ls --format '{{.Name}}|{{.Driver}}'")
    networks = []

    if not out:
        return networks

    for line in out.splitlines():
        parts = line.split("|")
        if len(parts) != 2:
            continue

        name, driver = parts
        networks.append({
            "name": name.strip(),
            "driver": driver.strip()
        })

    return networks


# ---------- MAIN PAGE ----------

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        action = request.form.get("action")

        # ---------- CREATE CONTAINER ----------
        if action == "create_container":
            image = request.form["image"]
            cname = request.form["container"]
            ctype = request.form["ctype"]

            status = container_status(cname)

            # 🔁 IF CONTAINER EXISTS
            if status == "running":
                flash(f"Container '{cname}' is already running.")
                return redirect(url_for("index"))

            if status == "exited":
                run_cmd(f"docker start {cname}")
                flash(f"Container '{cname}' was stopped and is now started.")
                return redirect(url_for("index"))

            # 🆕 CREATE NEW CONTAINER
            cmd = f"docker run --name {cname}"

            # -------- Linux --------
            if ctype == "linux":
                cmd += f" -it {image} bash"

            # -------- Database (KEEP RUNNING) --------
            elif ctype == "db":
                envs = request.form.get("envs")
                if envs:
                    for env in envs.split(","):
                        cmd += f" -e {env.strip()}"

                cmd += " --restart unless-stopped -d " + image

            # -------- Web --------
            elif ctype == "web":
                port_mode = request.form.get("port_mode")
                hp = request.form.get("hp")
                cp = request.form.get("cp")

                if port_mode == "manual" and hp and cp:
                    cmd += f" -p {hp}:{cp}"
                else:
                    cmd += " -P"

                cmd += " --restart unless-stopped -d " + image

            # -------- Volume --------
            volume = request.form.get("volume")
            mount = request.form.get("mount")
            if volume and mount:
                cmd += f" -v {volume}:{mount}"

            # -------- Network --------
            network = request.form.get("network")
            if network:
                cmd += f" --network {network}"

            flash(run_cmd(cmd))

        # ---------- CREATE VOLUME ----------
        elif action == "create_volume":
            vname = request.form["volume_name"]
            flash(run_cmd(f"docker volume create {vname}"))

        # ---------- CREATE NETWORK ----------
        elif action == "create_network":
            nname = request.form["network_name"]
            driver = request.form["driver"]
            flash(run_cmd(f"docker network create -d {driver} {nname}"))

    return render_template(
        "index.html",
        containers=get_containers(),
        images=get_images(),
        volumes=get_volumes(),
        networks=get_networks()
    )


# ---------- CONTAINER ACTIONS ----------

@app.route("/stop/<name>")
def stop(name):
    run_cmd(f"docker stop {name}")
    flash(f"{name} stopped")
    return redirect(url_for("index"))


@app.route("/restart/<name>")
def restart(name):
    run_cmd(f"docker start {name}")
    flash(f"{name} restarted")
    return redirect(url_for("index"))


@app.route("/remove/container/<name>")
def remove_container(name):
    run_cmd(f"docker rm -f {name}")
    flash(f"{name} removed")
    return redirect(url_for("index"))


@app.route("/logs/<name>")
def logs(name):
    logs = run_cmd(f"docker logs --tail 200 {name}")
    return render_template(
        "index.html",
        containers=get_containers(),
        images=get_images(),
        volumes=get_volumes(),
        networks=get_networks(),
        logs=logs,
        log_container=name
    )


# ---------- RESOURCE ACTIONS ----------

@app.route("/remove/image/<img_id>")
def remove_image(img_id):
    # 🔍 Find containers using this image
    containers = run_cmd(
        f"docker ps -a --filter ancestor={img_id} --format '{{{{.ID}}}}'"
    )

    # 🛑 Stop & 🗑️ Remove containers
    if containers:
        for cid in containers.splitlines():
            run_cmd(f"docker stop {cid}")
            run_cmd(f"docker rm {cid}")

    # 🧹 Remove image
    run_cmd(f"docker rmi -f {img_id}")
    flash("Image removed and all related containers stopped & deleted")

    return redirect(url_for("index"))


@app.route("/remove/volume/<name>")
def remove_volume(name):
    run_cmd(f"docker volume rm {name}")
    flash("Volume removed")
    return redirect(url_for("index"))


@app.route("/remove/network/<name>")
def remove_network(name):
    run_cmd(f"docker network rm {name}")
    flash("Network removed")
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)

