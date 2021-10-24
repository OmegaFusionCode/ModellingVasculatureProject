import InvasionPercolationNetwork.Cell

import scala.collection.mutable


class InvasionPercolationNetwork(x: Int, y: Int, occupancy: Float) {

    require(occupancy >= 0.0 && occupancy <= 1.0 && x>0 && y>0)

    private type Cell = InvasionPercolationNetwork.Cell

    // This is how many squares we fill.
    private val numToFill = scala.math.round(x * y * occupancy)

    private val r = new scala.util.Random()

    private val capacities = Array.fill(x)(Array.fill(y)(r.nextFloat()))

    // Make a cell for each space in the domain.
    private val cells: Array[Array[Cell]] = capacities.zipWithIndex.map {
        case (a,i) => a.zipWithIndex.map {
            case (b,j) => Cell(b, i, j)
        }
    }

    // The queue stores cells in the domain of the network, ordered by the strength of the cell.
    private val q = new mutable.PriorityQueue[Cell]()

    // A procedure to find the neighbours of a particular cell and add them to the priority queue.
    private def discoverNeighbours(c: Cell, step: Int): Unit = {
        val Cell(_, i, j) = c
        val neighbours = List((i-1, j), (i+1, j), (i, j-1), (i, j+1))
        for ((i2, j2) <- neighbours if i2 >= 0 && j2 >= 0 && i2 < x && j2 < y) {
            val c2 = cells(i2)(j2)
            if (!c2.isDiscovered) {
                c2.discovered = step
                q.enqueue(c2)
            }
        }
    }

    // (0, 0) is the first node to be added to the network
    cells(0)(0).discovered = 0
    q.enqueue(cells(0)(0))

    for (step <- 1 to numToFill) {

        // Add cell at front of queue to the network
        val c = q.dequeue()
        c.reached = step
        discoverNeighbours(c, step)
    }

    override def toString: String =
        cells.map(_.map(_.toString).mkString("")).mkString("\n")

}

object InvasionPercolationNetwork {

    private case class Cell(cap: Float, i: Int, j: Int) extends Ordered[Cell] {
        // Initially, a cell is undiscovered and unreached.
        var discovered: Int = -1
        var reached: Int = -1

        def isDiscovered: Boolean = reached != -1
        def isReached: Boolean = reached != -1

        // We order the cells by their strength in the priority queue.
        def compare(that: Cell): Int = this.cap compare that.cap

        override def toString: String = if (isReached) "███" else "   "
    }

    def make(x: Int, y: Int, occupancy: Float) = new InvasionPercolationNetwork(x, y, occupancy)

}