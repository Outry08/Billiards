#include "phylib.h"

/**
 * Function: phylib_new_still_ball
 * Description: Acts as a constructor for a new still ball.
 * @param number - The number for the new still ball
 * @param pos - The coordinates for the new still ball's position
 * @return - A pointer to the new still ball
**/
phylib_object* phylib_new_still_ball(unsigned char number, phylib_coord* pos) {

    phylib_object* sBall = malloc(sizeof(phylib_object));

    if(sBall == NULL)
        return NULL;

    sBall->type = PHYLIB_STILL_BALL;
    sBall->obj.still_ball.number = number;
    sBall->obj.still_ball.pos = *pos;

    return sBall;

}

/**
 * Function: phylib_new_rolling_ball
 * Description: Acts as a constructor for a new rolling ball.
 * @param number - The number for the new rolling ball
 * @param pos - The coordinates for the new rolling ball's position
 * @param vel - The coordinates for the new rolling ball's velocity
 * @param acc - The coordinates for the new rolling ball's acceleration
 * @return - A pointer to the new rolling ball
**/
phylib_object* phylib_new_rolling_ball(unsigned char number, phylib_coord* pos, phylib_coord* vel, phylib_coord* acc) {

    phylib_object* rBall = malloc(sizeof(phylib_object));

    if(rBall == NULL)
        return NULL;

    rBall->type = PHYLIB_ROLLING_BALL;
    rBall->obj.rolling_ball.number = number;
    rBall->obj.rolling_ball.pos = *pos;
    rBall->obj.rolling_ball.vel = *vel;
    rBall->obj.rolling_ball.acc = *acc;

    return rBall;

}

/**
 * Function: phylib_new_hole
 * Description: Acts as a constructor for a new hole.
 * @param pos - The coordinates for the new hole's position
 * @return - A pointer to the new hole
**/
phylib_object* phylib_new_hole(phylib_coord* pos) {

    phylib_object* hole = malloc(sizeof(phylib_object));

    if(hole == NULL)
        return NULL;

    hole->type = PHYLIB_HOLE;
    hole->obj.hole.pos = *pos;

    return hole;

}

/**
 * Function: phylib_new_hcushion
 * Description: Acts as a constructor for a new horizontal cushion.
 * @param y - The y-position of the new horizontal cushion
 * @return - A pointer to the new horizontal cushion
**/
phylib_object* phylib_new_hcushion(double y) {

    phylib_object* hCushion = malloc(sizeof(phylib_object));

    if(hCushion == NULL)
        return NULL;

    hCushion->type = PHYLIB_HCUSHION;
    hCushion->obj.hcushion.y = y;

    return hCushion;

}

/**
 * Function: phylib_new_vcushion
 * Description: Acts as a constructor for a new vertical cushion.
 * @param x - The x-position of the new vertical cushion
 * @return - A pointer to the new vertical cushion
**/
phylib_object* phylib_new_vcushion(double x) {

    phylib_object* vCushion = malloc(sizeof(phylib_object));

    if(vCushion == NULL)
        return NULL;

    vCushion->type = PHYLIB_VCUSHION;
    vCushion->obj.vcushion.x = x;

    return vCushion;

}

/**
 * Function: phylib_new_table
 * Description: Constructs a new table by calling all the other object constructors.
 * @return - A pointer to the new table
**/
phylib_table* phylib_new_table(void) {

    phylib_coord pos;
    phylib_table* table = malloc(sizeof(phylib_table));
    int count = 4;

    if(table == NULL)
        return NULL;

    //Making vcushions and hcushions
    table->time = 0.0;
    table->object[0] = phylib_new_hcushion(0.0);
    table->object[1] = phylib_new_hcushion(PHYLIB_TABLE_LENGTH);
    table->object[2] = phylib_new_vcushion(0.0);
    table->object[3] = phylib_new_vcushion(PHYLIB_TABLE_WIDTH);

    for(int i = 0; i < 2; i++) {
        for(int j = 0; j < 3; j++) {
            pos.x = i * 1350.0;
            pos.y = j * 1350.0;
            table->object[count] = phylib_new_hole(&pos);
            count++;
        }
    }

    //Initializing the rest of the objects to NULL
    for(int i = 10; i < PHYLIB_MAX_OBJECTS; i++)
        table->object[i] = NULL;

    return table;

}

/**
 * Function: phylib_copy_object
 * Description: Creates a copy of a given object.
 * @param dest - The destination that will point to the new copy of the object
 * @param src - The object that will be copied
**/
void phylib_copy_object(phylib_object** dest, phylib_object** src) {
    if(*src == NULL) {
        *dest = NULL;
        return;
    }

    *dest = malloc(sizeof(phylib_object));
    memcpy(*dest, *src, sizeof(phylib_object));
}

/**
 * Function: phylib_copy_table
 * Description: Creates a copy of the given table.
 * @param table - The table that will be copied
 * @return - A pointer to the copy of the given table
**/
phylib_table* phylib_copy_table(phylib_table* table) {
    phylib_table* newTable;

    newTable = malloc(sizeof(phylib_table));
    if(newTable == NULL)
        return NULL;

    //Copying each object
    for(int i = 0; i < PHYLIB_MAX_OBJECTS; i++)
        phylib_copy_object(&(newTable->object[i]), &(table->object[i]));

    newTable->time = table->time;

    return newTable;
}

/**
 * Function: phylib_add_object
 * Description: Adds the given object to the given table.
 * @param table - The table to be added to
 * @param object - The object to be added
**/
void phylib_add_object(phylib_table* table, phylib_object* object) {
    for(int i = 0; i < PHYLIB_MAX_OBJECTS; i++) {
        if(table->object[i] == NULL) {
            table->object[i] = object;
            return;
        }
    }
}

/**
 * Function: phylib_free_table
 * Description: Frees memory of each object in the table, and the memory for the table itself.
 * @param table - The table to be freed
**/
void phylib_free_table(phylib_table* table) {
    for(int i = 0; i < PHYLIB_MAX_OBJECTS; i++) {
        if(table->object[i] != NULL)
            free(table->object[i]);
    }

    free(table);
}

/**
 * Function: phylib_sub
 * Description: Makes a new coordinate that is the result of subtracting the two given coordinates.
 * @param c1 - The coordinate being subtracted from
 * @param c2 - The coordinate subtracting from c1
 * @return - The coordinate of the different between the two coordinates
**/
phylib_coord phylib_sub(phylib_coord c1, phylib_coord c2) {
    phylib_coord diff;
    diff.x = c1.x - c2.x;
    diff.y = c1.y - c2.y;
    return diff;
}

/**
 * Function: phylib_length
 * Description: Calculates the magnitude of the given coordinate.
 * @param c - The coordinate to have its length be calculated
 * @return - The magnitude of the given coordinate
**/
double phylib_length(phylib_coord c) {
    //Magnitude = sqrt((c.x)^2 + (c.y)^2)
    return sqrt((c.x * c.x) + (c.y * c.y));
}

/**
 * Function: phylib_dot_product
 * Description: Calculates the dot product between two coordinates.
 * @param a - Coordinate 1
 * @param b - Coordinate 2
 * @return - The dot product bewteen the two vectors
**/
double phylib_dot_product(phylib_coord a, phylib_coord b) {
    return (a.x * b.x) + (a.y * b.y);
}

/**
 * Function: phylib_distance
 * Description: Calculates the distance between a rolling ball and whatever the other object is.
 * @param obj1 - The object that should be a rolling ball
 * @param obj2 - The object from which the distance from the rolling ball will be taken
 * @return - The distance between the two objects
**/
double phylib_distance(phylib_object* obj1, phylib_object* obj2) {

    //NULL CHECKS?????????
    if(obj1->type != PHYLIB_ROLLING_BALL)
        return -1.0;

    double distance;

    //Distance calculation based on what object type obj2 is
    switch(obj2->type) {
        case PHYLIB_ROLLING_BALL:
            distance = phylib_length(phylib_sub(obj1->obj.rolling_ball.pos, obj2->obj.rolling_ball.pos)) - PHYLIB_BALL_DIAMETER;
            break;

        case PHYLIB_STILL_BALL:
            distance = phylib_length(phylib_sub(obj1->obj.rolling_ball.pos, obj2->obj.still_ball.pos)) - PHYLIB_BALL_DIAMETER;
            break;

        case PHYLIB_HOLE:
            distance = phylib_length(phylib_sub(obj1->obj.rolling_ball.pos, obj2->obj.hole.pos)) - PHYLIB_HOLE_RADIUS;
            break;

        case PHYLIB_HCUSHION:
            distance = fabs(obj1->obj.rolling_ball.pos.y - obj2->obj.hcushion.y) - PHYLIB_BALL_RADIUS;
            break;

        case PHYLIB_VCUSHION:
            distance = fabs(obj1->obj.rolling_ball.pos.x - obj2->obj.vcushion.x) - PHYLIB_BALL_RADIUS;
            break;

        default:
            distance = -1.0;
            break;
    }

    return distance;
}

/**
 * Function: phylib_roll
 * Description: Calculates the new position, velocity, and acceleration of a rolling ball based on its
   previous position, velocity, and acceleration.
 * @param new - The object for the ball's new information after rolling
 * @param old - The ball's current information before rolling
 * @param time - The elapsed time between the ball's old state and the ball's new state
**/
void phylib_roll(phylib_object* new, phylib_object* old, double time) {

    if(old->type != PHYLIB_ROLLING_BALL || new->type != PHYLIB_ROLLING_BALL)
        return;

    //p = p1 + v1*t + a1*t^2
    new->obj.rolling_ball.pos.x = old->obj.rolling_ball.pos.x + old->obj.rolling_ball.vel.x * time + old->obj.rolling_ball.acc.x * time * time / 2;
    new->obj.rolling_ball.pos.y = old->obj.rolling_ball.pos.y + old->obj.rolling_ball.vel.y * time + old->obj.rolling_ball.acc.y * time * time / 2;

    //v = v1 + a1*t
    new->obj.rolling_ball.vel.x = old->obj.rolling_ball.vel.x + old->obj.rolling_ball.acc.x * time;
    new->obj.rolling_ball.vel.y = old->obj.rolling_ball.vel.y + old->obj.rolling_ball.acc.y * time;

    if((old->obj.rolling_ball.vel.x > 0 && new->obj.rolling_ball.vel.x <= 0) || (old->obj.rolling_ball.vel.x < 0 && new->obj.rolling_ball.vel.x >= 0)) {
        new->obj.rolling_ball.vel.x = 0;
        new->obj.rolling_ball.acc.x = 0;
    }
    if((old->obj.rolling_ball.vel.y > 0 && new->obj.rolling_ball.vel.y <= 0) || (old->obj.rolling_ball.vel.y < 0 && new->obj.rolling_ball.vel.y >= 0)) {
        new->obj.rolling_ball.vel.y = 0;
        new->obj.rolling_ball.acc.y = 0;
    }

}

/**
 * Function: phylib_stopped
 * Description: Checks if the object is a rolling ball that has stopped rolling. If it has, it changes it to a still ball.
 * @param object - The object that's being checked if it's stopped
 * @return - 1 if the ball has stopped, 0 if the ball hasn't stopped
**/
unsigned char phylib_stopped(phylib_object* object) {

    if(object != NULL && phylib_length(object->obj.rolling_ball.vel) < PHYLIB_VEL_EPSILON) {
        object->obj.still_ball.number = object->obj.rolling_ball.number;
        object->obj.still_ball.pos.x = object->obj.rolling_ball.pos.x;
        object->obj.still_ball.pos.y = object->obj.rolling_ball.pos.y;
        object->type = PHYLIB_STILL_BALL;
        return 1;
    }
    return 0;
}

/**
 * Function: phylib_bounce
 * Description: Calculates and executes the behviours of collisions between different combinations of objects.
 * @param a - An object that is assumed to be a rolling ball.
 * @param b - An object whose type can be anything.
**/
void phylib_bounce(phylib_object** a, phylib_object** b) {
    switch((*b)->type) {

        //Collision with a horizontal cushion
        case PHYLIB_HCUSHION:
            (*a)->obj.rolling_ball.vel.y *= -1;
            (*a)->obj.rolling_ball.acc.y *= -1;
            break;

            //Collision with a vertical cushion
        case PHYLIB_VCUSHION:
            (*a)->obj.rolling_ball.vel.x *= -1;
            (*a)->obj.rolling_ball.acc.x *= -1;
            break;

            //Collision with a hole
        case PHYLIB_HOLE:
            free(*a);
            *a = NULL;
            break;

            //Collision with a still ball
        case PHYLIB_STILL_BALL:
            (*b)->obj.rolling_ball.pos.x = (*b)->obj.still_ball.pos.x;
            (*b)->obj.rolling_ball.pos.y = (*b)->obj.still_ball.pos.y;
            (*b)->obj.rolling_ball.number = (*b)->obj.still_ball.number;
            (*b)->obj.rolling_ball.vel.x = 0.0;
            (*b)->obj.rolling_ball.vel.y = 0.0;
            (*b)->obj.rolling_ball.acc.x = 0.0;
            (*b)->obj.rolling_ball.acc.y = 0.0;
            (*b)->type = PHYLIB_ROLLING_BALL;

            //Collision with another rolling ball
        case PHYLIB_ROLLING_BALL: {
            phylib_coord r_ab = phylib_sub((*a)->obj.rolling_ball.pos, (*b)->obj.rolling_ball.pos);
            phylib_coord v_rel = phylib_sub((*a)->obj.rolling_ball.vel, (*b)->obj.rolling_ball.vel);
            phylib_coord n;
            n.x = r_ab.x / phylib_length(r_ab);
            n.y = r_ab.y / phylib_length(r_ab);
            double v_rel_n = phylib_dot_product(v_rel, n);

            (*a)->obj.rolling_ball.vel.x -= v_rel_n * n.x;
            (*a)->obj.rolling_ball.vel.y -= v_rel_n * n.y;

            (*b)->obj.rolling_ball.vel.x += v_rel_n * n.x;
            (*b)->obj.rolling_ball.vel.y += v_rel_n * n.y;

            double aSpeed = phylib_length((*a)->obj.rolling_ball.vel);
            double bSpeed = phylib_length((*b)->obj.rolling_ball.vel);

            if(aSpeed > PHYLIB_VEL_EPSILON) {
                (*a)->obj.rolling_ball.acc.x = -1 * (*a)->obj.rolling_ball.vel.x / aSpeed * PHYLIB_DRAG;
                (*a)->obj.rolling_ball.acc.y = -1 * (*a)->obj.rolling_ball.vel.y / aSpeed * PHYLIB_DRAG;
            }
            if(bSpeed > PHYLIB_VEL_EPSILON) {
                (*b)->obj.rolling_ball.acc.x = -1 * (*b)->obj.rolling_ball.vel.x / bSpeed * PHYLIB_DRAG;
                (*b)->obj.rolling_ball.acc.y = -1 * (*b)->obj.rolling_ball.vel.y / bSpeed * PHYLIB_DRAG;
            }
            break;
        }

    }
}

/**
 * Function: phylib_rolling
 * Description: Counts how many rolling balls are on the table.
 * @param t - The table being checked
 * @return - The number of rolling balls
**/
unsigned char phylib_rolling(phylib_table* t) {

    int count = 0;

    for(int i = 0; i < PHYLIB_MAX_OBJECTS; i++)
        if(t->object[i] != NULL && t->object[i]->type == PHYLIB_ROLLING_BALL)
            count++;

    return count;
}

/**
 * Function: phylib_segment
 * Description: Simulates the rolling of balls and their eventual collisions, one frame of time at a time.
   It halts the simulation to print snapshots of the current turn after any collisions occur, any balls stop rolling, or the maximum time elapses.
 * @param table - The table for the current state of the game
 * @return - A copy of the given table after the current chunk of the simulation finishes
**/
phylib_table* phylib_segment(phylib_table* table) {
    if(phylib_rolling(table) == 0)
        return NULL;

    phylib_table* tableCopy = phylib_copy_table(table);

    int shouldExit = 0;
    int t = 1;

    //Loops until a significant event occurs or the maximum time elapses
    for(t = 1; t * PHYLIB_SIM_RATE < PHYLIB_MAX_TIME && !shouldExit; t++) {

        //Loop to roll all the rolling balls on the table one more frame forward
        for(int i = 0; i < PHYLIB_MAX_OBJECTS; i++)
            if(tableCopy->object[i] != NULL && tableCopy->object[i]->type == PHYLIB_ROLLING_BALL)
                phylib_roll(tableCopy->object[i], table->object[i], t * PHYLIB_SIM_RATE);

        //Another loop used to check for collisions for each rolling ball.
        for(int i = 0; i < PHYLIB_MAX_OBJECTS; i++) {
            if(tableCopy->object[i] != NULL && tableCopy->object[i]->type == PHYLIB_ROLLING_BALL && table->object[i]->type == PHYLIB_ROLLING_BALL) {
                //Loop to check all other table objects for collisions with the current rolling ball object
                for(int j = 0; j < PHYLIB_MAX_OBJECTS; j++) {
                    if(j != i && tableCopy->object[i] != NULL && tableCopy->object[j] != NULL && phylib_distance(tableCopy->object[i], tableCopy->object[j]) < 0.0) {
                        //This if statement prevents a collision between two rolling balls to be registered twice. 
                        if(!(tableCopy->object[i]->type == PHYLIB_ROLLING_BALL && tableCopy->object[j]->type == PHYLIB_ROLLING_BALL && j < i)) {
                            shouldExit = 1;
                            phylib_bounce(&(tableCopy->object[i]), &(tableCopy->object[j]));
                        }
                    }
                }
                //Checking if any rolling balls have stopped rolling
                if(phylib_stopped(tableCopy->object[i]))
                    shouldExit = 1;
            }
        }
    }

    //Adding the elapsed time to the table's total time variable
    tableCopy->time += t * PHYLIB_SIM_RATE;

    return tableCopy;

}

char* phylib_object_string(phylib_object* object) {
    static char string[80];
    if(object == NULL) {
        snprintf(string, 80, "NULL;");
        return string;
    }
    switch(object->type) {
        case PHYLIB_STILL_BALL:
            snprintf(string, 80,
                "STILL_BALL (%d,%6.1lf,%6.1lf)",
                object->obj.still_ball.number,
                object->obj.still_ball.pos.x,
                object->obj.still_ball.pos.y);
            break;
        case PHYLIB_ROLLING_BALL:
            snprintf(string, 80,
                "ROLLING_BALL (%d,%6.1lf,%6.1lf,%6.1lf,%6.1lf,%6.1lf,%6.1lf)",
                object->obj.rolling_ball.number,
                object->obj.rolling_ball.pos.x,
                object->obj.rolling_ball.pos.y,
                object->obj.rolling_ball.vel.x,
                object->obj.rolling_ball.vel.y,
                object->obj.rolling_ball.acc.x,
                object->obj.rolling_ball.acc.y);
            break;
        case PHYLIB_HOLE:
            snprintf(string, 80,
                "HOLE (%6.1lf,%6.1lf)",
                object->obj.hole.pos.x,
                object->obj.hole.pos.y);
            break;
        case PHYLIB_HCUSHION:
            snprintf(string, 80,
                "HCUSHION (%6.1lf)",
                object->obj.hcushion.y);
            break;
        case PHYLIB_VCUSHION:
            snprintf(string, 80,
                "VCUSHION (%6.1lf)",
                object->obj.vcushion.x);
            break;
    }
    return string;
}
