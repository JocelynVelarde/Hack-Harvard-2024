'use client'

import React, { useState, useRef } from "react"
import { Loader2, Camera, Upload } from "lucide-react"

import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Textarea } from "@/components/ui/textarea"

export default function HomePage() {
  const [uploadedImage, setUploadedImage] = useState(null)
  const [sentimentAnalysis, setSentimentAnalysis] = useState("")
  const [heatmapImage, setHeatmapImage] = useState(null)
  const [isAnalyzing, setIsAnalyzing] = useState(false)
  const fileInputRef = useRef(null)

  // Mocked API calls - replace these with actual API calls in a real application
  const analyzeSentiment = async (imageUrl) => {
    await new Promise(resolve => setTimeout(resolve, 1000))
    return "The image shows a busy street corner with several pedestrians. There appears to be no immediate security threats visible."
  }

  const generateHeatmap = async (imageUrl) => {
    await new Promise(resolve => setTimeout(resolve, 1000))
    return "/placeholder.svg?height=300&width=400"
  }

  const handleFileChange = async (event) => {
    const file = event.target.files[0]
    if (file) {
      const reader = new FileReader()
      reader.onload = async (e) => {
        setUploadedImage(e.target.result)
        setIsAnalyzing(true)
        
        try {
          const sentiment = await analyzeSentiment(e.target.result)
          setSentimentAnalysis(sentiment)
          
          const heatmap = await generateHeatmap(e.target.result)
          setHeatmapImage(heatmap)
        } catch (error) {
          console.error("Error analyzing image:", error)
        } finally {
          setIsAnalyzing(false)
        }
      }
      reader.readAsDataURL(file)
    }
  }

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-3xl font-bold mb-6">TheftWatch</h1>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <Card>
          <CardHeader>
            <CardTitle>Upload Security Footage</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="flex items-center justify-center w-full">
              <Label
                htmlFor="file-upload"
                className="flex flex-col items-center justify-center w-full h-64 border-2 border-dashed rounded-lg cursor-pointer bg-gray-50 hover:bg-gray-100 dark:bg-gray-700 dark:border-gray-600 dark:hover:bg-gray-600"
              >
                <div className="flex flex-col items-center justify-center pt-5 pb-6">
                  <Upload className="w-8 h-8 mb-4 text-gray-500 dark:text-gray-400" />
                  <p className="mb-2 text-sm text-gray-500 dark:text-gray-400">
                    <span className="font-semibold">Click to upload</span> or drag and drop
                  </p>
                  <p className="text-xs text-gray-500 dark:text-gray-400">
                    SVG, PNG, JPG or GIF (MAX. 800x400px)
                  </p>
                </div>
                <Input
                  id="file-upload"
                  type="file"
                  className="hidden"
                  onChange={handleFileChange}
                  ref={fileInputRef}
                  accept="image/*"
                />
              </Label>
            </div>
            {uploadedImage && (
              <div className="mt-4">
                <img src={uploadedImage} alt="Uploaded security footage" className="w-full h-auto rounded-lg" />
              </div>
            )}
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Sentiment Analysis</CardTitle>
          </CardHeader>
          <CardContent>
            <Textarea
              placeholder="Sentiment analysis will appear here..."
              value={sentimentAnalysis}
              readOnly
              className="h-40"
            />
            {isAnalyzing && (
              <div className="flex items-center justify-center mt-4">
                <Loader2 className="h-6 w-6 animate-spin" />
                <span className="ml-2">Analyzing...</span>
              </div>
            )}
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Risk Heatmap</CardTitle>
          </CardHeader>
          <CardContent>
            {heatmapImage ? (
              <img src={heatmapImage} alt="Risk heatmap" className="w-full h-auto rounded-lg" />
            ) : (
              <div className="h-[300px] flex items-center justify-center bg-muted rounded-lg">
                <p>Heatmap will appear here after analysis</p>
              </div>
            )}
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Camera Locations</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="relative w-full h-[300px] bg-muted rounded-lg overflow-hidden">
              <svg viewBox="0 0 100 100" className="w-full h-full">
                <rect x="0" y="0" width="100" height="100" fill="#e2e8f0" />
                <circle cx="20" cy="20" r="3" fill="#3b82f6" />
                <circle cx="80" cy="30" r="3" fill="#3b82f6" />
                <circle cx="50" cy="70" r="3" fill="#3b82f6" />
                <circle cx="10" cy="90" r="3" fill="#3b82f6" />
              </svg>
              <div className="absolute top-2 left-2 bg-white p-2 rounded shadow text-sm">
                <div className="flex items-center">
                  <Camera className="h-4 w-4 mr-2" />
                  <span>Camera Locations</span>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      <Card className="mt-6">
        <CardHeader>
          <CardTitle>Add New Camera</CardTitle>
        </CardHeader>
        <CardContent>
          <form className="space-y-4">
            <div className="grid grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label htmlFor="camera-name">Camera Name</Label>
                <Input id="camera-name" placeholder="Enter camera name" />
              </div>
              <div className="space-y-2">
                <Label htmlFor="camera-location">Location</Label>
                <Input id="camera-location" placeholder="Enter camera location" />
              </div>
            </div>
            <Button type="submit" className="w-full">Add Camera</Button>
          </form>
        </CardContent>
      </Card>
    </div>
  )
}