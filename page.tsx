"use client"

import { useState, useRef } from "react"
import { Play, Square, Pause } from "lucide-react"
import { Button } from "@/components/ui/button"

export default function CodeRot() {
  const [code, setCode] = useState("")
  const [output, setOutput] = useState("")
  const [isRunning, setIsRunning] = useState(false)
  const [isPaused, setIsPaused] = useState(false)
  const executionTimerRef = useRef<NodeJS.Timeout | null>(null)
  const executionIntervalRef = useRef<NodeJS.Timeout | null>(null)

  const handleRun = () => {
    if (isPaused) {
      // Resume execution
      setIsPaused(false)
      return
    }

    // Clear any existing timers
    if (executionTimerRef.current) {
      clearTimeout(executionTimerRef.current)
    }
    if (executionIntervalRef.current) {
      clearInterval(executionIntervalRef.current)
    }

    setIsRunning(true)
    setOutput("Running your beautifully bad code...\n")

    // Simulate code execution with periodic updates
    let executionStep = 0
    const steps = [
      "Initializing bad practices...",
      "Ignoring all best practices...",
      "Implementing anti-patterns...",
      "Creating memory leaks...",
      "Successfully rotted your code!",
    ]

    executionIntervalRef.current = setInterval(() => {
      if (executionStep < steps.length) {
        setOutput((prev) => prev + steps[executionStep] + "\n")
        executionStep++
      } else {
        if (executionIntervalRef.current) {
          clearInterval(executionIntervalRef.current)
        }
      }
    }, 800)
  }

  const handleStop = () => {
    if (executionTimerRef.current) {
      clearTimeout(executionTimerRef.current)
      executionTimerRef.current = null
    }
    if (executionIntervalRef.current) {
      clearInterval(executionIntervalRef.current)
      executionIntervalRef.current = null
    }

    setIsRunning(false)
    setIsPaused(false)
    setOutput("")
  }

  const handlePause = () => {
    if (isRunning) {
      if (isPaused) {
        // Resume execution
        setIsPaused(false)
        // Execution would resume here in a real implementation
      } else {
        // Pause execution
        setIsPaused(true)
        // Execution would pause here in a real implementation
        if (executionIntervalRef.current) {
          clearInterval(executionIntervalRef.current)
          executionIntervalRef.current = null
        }
        setOutput((prev) => prev + "Execution paused...\n")
      }
    }
  }

  return (
    <main className="min-h-screen bg-[#13111C] text-white p-8 relative overflow-hidden">
      {/* Background ellipses */}
      <div className="absolute top-[-200px] left-[-100px] w-[600px] h-[600px] rounded-[2711px] bg-[rgba(195,24,229,0.18)] blur-[200px]"></div>
      <div className="absolute bottom-[-200px] right-[-100px] w-[600px] h-[600px] rounded-[2422px] bg-[#C318E5] opacity-20 blur-[200px]"></div>

      {/* Header */}
      <div className="text-center mb-8 relative z-10">
        <h1 className="text-4xl font-bold mb-2">
          <span className="text-[#F5F5DC]">codeRot</span>
        </h1>
        <p className="text-[#9D8EC7]">build code, the bad way</p>
      </div>

      {/* Editor */}
      <div className="relative mb-4 z-10">
        <div className="absolute -inset-0.5 bg-[#B026FF] rounded-lg blur opacity-75"></div>
        <div className="relative">
          <textarea
            value={code}
            onChange={(e) => setCode(e.target.value)}
            className="w-full h-64 bg-[#1A1825] rounded-lg p-4 font-mono text-[#F5F5DC] focus:outline-none resize-none"
            placeholder="Write your worst code here..."
          />
          <Button
            onClick={handleRun}
            className="absolute top-2 right-2 bg-green-500 hover:bg-green-600 rounded-full w-8 h-8 p-0"
          >
            <Play className="h-4 w-4" />
          </Button>
        </div>
      </div>

      {/* Output */}
      <div className="relative z-10">
        <div className="absolute -inset-0.5 bg-[#B026FF] rounded-lg blur opacity-75"></div>
        <div className="relative bg-[#1A1825] rounded-lg p-4">
          <div className="flex items-center justify-between mb-2">
            <span className="text-[#9D8EC7] font-mono">veiny ahh output</span>
            <div className="space-x-2">
              <Button
                onClick={handleRun}
                disabled={isRunning && !isPaused}
                className="bg-green-500 hover:bg-green-600 rounded-full w-8 h-8 p-0"
              >
                <Play className="h-4 w-4" />
              </Button>
              <Button
                onClick={handleStop}
                disabled={!isRunning}
                className="bg-red-500 hover:bg-red-600 rounded-full w-8 h-8 p-0"
              >
                <Square className="h-4 w-4" />
              </Button>
              <Button
                onClick={handlePause}
                disabled={!isRunning}
                className={`${isPaused ? "bg-green-500 hover:bg-green-600" : "bg-yellow-500 hover:bg-yellow-600"} rounded-full w-8 h-8 p-0`}
              >
                <Pause className="h-4 w-4" />
              </Button>
            </div>
          </div>
          <pre className="font-mono text-[#F5F5DC] min-h-[100px] whitespace-pre-wrap">
            {output || "Output will appear here..."}
          </pre>
        </div>
      </div>
    </main>
  )
}

