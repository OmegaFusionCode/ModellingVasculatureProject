import InvasionPercolationNetwork.Cell

import scala.collection.mutable


class InvasionPercolationNetwork(x: Int, y: Int, occupancy: Float) {

    require(occupancy >= 0.0 && occupancy <= 1.0)

    private type Cell = InvasionPercolationNetwork.Cell
    //private type IPCell = InvasionPercolationNetwork.IPCell

    // This is how many squares we fill. We round
    private val numToFill = scala.math.round(x * y * occupancy)

    private val r = new scala.util.Random()

    def makeNewNetwork(): Array[Array[Boolean]] = {

        val capacities = Array.fill(x)(Array.fill(y)(r.nextFloat()))

        // pair each capacity with its index
        val indices: Array[Array[Cell]] = capacities.zipWithIndex.map {
            case (a,i) => a.zipWithIndex.map {
                case (b,j) => new Cell(b, i, j)
            }
        }

        // The queue stores, as a pair, the capacity of the cell and its index
        val q = new mutable.PriorityQueue[Cell]()

        val inQueue, inNetwork = Array.ofDim[Boolean](x, y)

        val cells = Array.ofDim[Cell](x, y)
        // (0, 0) is in the network initially
        inNetwork(0)(0)= true
        // This means that (0, 1) and (1, 0) are scheduled to be added
        inQueue(0)(0) = true
        inQueue(0)(1) = true
        inQueue(1)(0) = true
        q.enqueue(indices(1)(0))
        q.enqueue(indices(0)(1))

        for (_ <- 2 to numToFill) {

            // Add cell at front of queue to the network
            val Cell(_, i, j) = q.dequeue()

            inNetwork(i)(j) = true

            // add adjacent cells
            if (i > 0 && !inQueue(i-1)(j)) {
                inQueue(i-1)(j) = true
                q.enqueue(indices(i-1)(j))
            }
            if (i < x-1 && !inQueue(i+1)(j)) {
                inQueue(i+1)(j) = true
                q.enqueue(indices(i+1)(j))
            }
            if (j > 0 && !inQueue(i)(j-1)) {
                inQueue(i)(j-1) = true
                q.enqueue(indices(i)(j-1))
            }
            if (j < y-1 && !inQueue(i)(j+1)) {
                inQueue(i)(j+1) = true
                q.enqueue(indices(i)(j+1))
            }
        }
        inNetwork
    }

}

object InvasionPercolationNetwork {

    private case class Cell(cap: Float, i: Int, j: Int) extends Ordered[Cell] {
        var discovered: Int = -1
        var reached: Int = -1
        def compare(that: Cell): Int = this.cap compare that.cap
    }

    def draw(a: Array[Array[Boolean]]): Unit =
        println(a.map(_.map(if (_) "██" else "  ").mkString("")).mkString("\n"))


}