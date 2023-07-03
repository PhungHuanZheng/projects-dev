let target;
let projectiles = [];


function setup() {
    createCanvas(windowWidth, windowHeight);

    target = new Target(width / 2, height / 2);
    target.vel = createVector(3, 6)
}

function draw() {
    background(0);

    if (frameCount % 1 === 0) {
        let newProj = new Projectile(0, height / 2, 500);
        newProj.vel.x = random(40, 100);
        newProj.vel.y = random(-5, 5);
        newProj.initialMag = newProj.vel.mag()

        projectiles.push(newProj)

        newProj = new Projectile(width, height / 2, 500);
        newProj.vel.x = random(-40, -100);
        newProj.vel.y = random(-5, 5)
        newProj.initialMag = newProj.vel.mag()

        projectiles.push(newProj)
    }

    for (let i = projectiles.length - 1; i >= 0; i--) {
        projectiles[i].home(target);
        projectiles[i].show(color(map(i, 0, projectiles.length, 0, 255), map(i, 0, projectiles.length, 255, 0), 0))

        if (
            dist(projectiles[i].pos.x, projectiles[i].pos.y, target.pos.x, target.pos.y) < 10 ||
            projectiles[i].pos.x < 0 || projectiles[i].pos.x > width ||
            projectiles[i].pos.y < 0 || projectiles[i].pos.y > height
        ) {
            projectiles.splice(i, 1)
        }
    }

    target.update()
    target.show()
}