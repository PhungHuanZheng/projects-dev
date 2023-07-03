let target;
let projectiles = [];


function setup() {
    createCanvas(windowWidth, windowHeight);

    target = new Target(width / 2, height / 2);
    target.vel = createVector(noise(target.pos.x, target.pos.x), noise(target.pos.y, target.pos.y))
}

function draw() {
    background(0);

    // if (frameCount % 20 === 0) {
    //     let newProj = new Projectile(0, height / 2, 500);
    //     newProj.vel.x = random(40, 100);
    //     newProj.vel.y = random(-5, 5);
    //     newProj.initialMag = newProj.vel.mag()

    //     projectiles.push(newProj)

    //     newProj = new Projectile(width, height / 2, 500);
    //     newProj.vel.x = random(-40, -100);
    //     newProj.vel.y = random(-5, 5)
    //     newProj.initialMag = newProj.vel.mag()

    //     projectiles.push(newProj)
    // }

    // if (mouseIsPressed) {
        if (frameCount % 1 === 0) {
            let newProj = new Projectile(width / 2, height / 2, 1500);
            // let newProj = new Projectile(mouseX, mouseY, 1500);
            newProj.vel.x = random(-50, 50);
            newProj.vel.y = random(-50, 50);

            projectiles.push(newProj)
        }
    // }

    for (let i = projectiles.length - 1; i >= 0; i--) {
        projectiles[i].home(target);
        
        let d = dist(projectiles[i].pos.x, projectiles[i].pos.y, target.pos.x, target.pos.y)
        if (
            d < 10 ||
            projectiles[i].pos.x < - width || projectiles[i].pos.x > width * 2 ||
            projectiles[i].pos.y < - height || projectiles[i].pos.y > height * 2
        ) {
            projectiles.splice(i, 1);
            continue;
        }

        projectiles[i].show(color(map(d, 0, 500, 0, 255), map(d, 0, 500, 255, 0), 0))
    } 

    target.acc.add(
        [0, -1, 1][floor(random(3))] * noise(target.pos.x, target.pos.x),
        [0, -1, 1][floor(random(3))] * noise(target.pos.y, target.pos.y),
    )

    target.update()
    target.show()
}